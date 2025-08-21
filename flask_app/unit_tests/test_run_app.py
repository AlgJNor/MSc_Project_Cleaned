import os
import sys
import tempfile
import csv
import pytest
from unittest.mock import patch
from werkzeug.security import generate_password_hash


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from flask_app import run_app
from flask_app.auth.models import User, database


@pytest.fixture()
def client():
    # use a truly isolated temp DB per test run
    fd, db_path = tempfile.mkstemp()
    app = run_app.app
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        # helpful for sqlite + Flask in tests
        SQLALCHEMY_ENGINE_OPTIONS={"connect_args": {"check_same_thread": False}},
    )

    with app.app_context():
        # start from a clean slate even if the app already created/bound the engine
        database.session.remove()
        database.drop_all()
        database.create_all()

        # seed admin only if it doesn't already exist (app may auto-seed)
        if not User.query.filter_by(username="admin").first():
            database.session.add(
                User(
                    email="admin@gmail.com",
                    username="admin",
                    password_hash=generate_password_hash("test123"),
                    role="admin",
                )
            )
            database.session.commit()

    # return a test client (so .get/.post work)
    with app.test_client() as c:
        yield c

    os.close(fd)
    os.unlink(db_path)


def login(client, username, password):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def test_admin_requires_login_for_logged_in_user(client):
    resp = client.get("/classification_log.html")
    assert resp.status_code in (302, 401, 403)


def test_register_and_login_flow(client):
    resp = client.post(
        "/register",
        data={"username": "newuser", "email": "example@gmail.com", "password": "test123"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    resp = login(client, "newuser", "test123")
    assert resp.status_code == 200

@pytest.fixture()
def admin_client_with_temp_log(client, tmp_path):
    fd, log_path = tempfile.mkstemp()
    os.close(fd)
    with open(log_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(
            ["Timestamp", "Email Text", "Prediction", "Confidence Score", "Top Contributing Words"]
        )
    run_app.LOG_PATH = log_path

    login(client, "admin", "test123")

    try:
        yield client, log_path
    finally:
        os.remove(log_path)

@pytest.fixture()
def admin_client_with_predefined_logs(admin_client_with_temp_log):
    """Same as the admin_client_with_log but we prepopulatre teow rows for search terms"""
    client, log_path = admin_client_with_temp_log

    rows = [
        ["2025-08-20 10:00:00", "please send that invoice asap", "Phishing", 93.5, "invoice, review"],
        ["2025-08-20 12:00:00", "we have a team meeting this evening", "Not Phishing", 8.5, "meeting"]
    ]

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    return client, str(log_path)


def test_home_post_classified_logs(admin_client_with_temp_log):
    client, log_path = admin_client_with_temp_log

    fake_prediction = {
        "label": "Phishing",
        "confidence_score": 98.0,
        "top_contributing_words": [
            {"word": "urgent", "weight": 60},
            {"word": "account", "weight": 35},
        ]
    }
    email_text = "verify your account"
    with patch("flask_app.run_app.predict_email", return_value=fake_prediction):
        response = client.post("/", data={"email_text": "Urgent: please verify your account"}, follow_redirects=True)


    assert response.status_code == 200
    assert b"RESULT:" in response.data
    assert b"Phishing" in response.data
    assert b"98" in response.data
    assert b"urgent" in response.data
    assert b"account" in response.data


    with open(log_path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["Timestamp", "Email Text", "Prediction", "Confidence Score", "Top Contributing Words"]
    assert any(email_text in col for row in rows for col in row)



def test_classification_log_search_filters_invoice(admin_client_with_predefined_logs):
    client, log_path = admin_client_with_predefined_logs
    response = client.get("/classification_log.html?q=invoice")
    assert response.status_code == 200
    html = response.data.decode("utf8").lower()
    assert "please send that invoice asap" in html
    assert "we have a team meeting this evening" not in html

def test_classification_log_search_filters_meeting(admin_client_with_predefined_logs):
    client, log_path = admin_client_with_predefined_logs
    response = client.get("/classification_log.html?q=meeting")
    assert response.status_code == 200
    html = response.data.decode("utf8").lower()
    assert "we have a team meeting this evening" in html
    assert "please send that invoice asap" not in html

def test_classification_log_search_no_query_shows_all(admin_client_with_predefined_logs):
    client, _ = admin_client_with_predefined_logs
    response = client.get("/classification_log.html")
    assert response.status_code == 200
    html = response.data.decode("utf8").lower()
    assert "we have a team meeting this evening" in html
    assert "please send that invoice asap" in html

