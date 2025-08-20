import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import csv

from flask import Flask, request, render_template, abort, flash, redirect, url_for
from datetime import datetime

from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from functools import wraps
from flask_app.auth.models import database, User
from flask_sqlalchemy import SQLAlchemy
from flask_app.extensions import bcrypt
import sys
import os
os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app','predict.py'))
from app.predict import predict_email
from werkzeug.security import generate_password_hash, check_password_hash
import re
import ast

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    from flask_login import current_user
    return dict(current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful.', 'danger')
    return render_template('login.html')

def is_email_valid(email):
    pattern  = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern,email)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not is_email_valid(email):
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('register'))

        if not username:
            flash('Please enter a username.', 'danger')
            return redirect(url_for('register'))

        if not password or not confirm_password:
            flash('Please enter and confirm your password.', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exits. Please choose another suername.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('That email already exits. Please choose another email.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_saved_user = User(username=username, email=email, password_hash=hashed_password)
        database.session.add(new_saved_user)
        database.session.commit()

        flash('Thank you for registering. Please login to continue.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        email_text = request.form.get("email_text")
        if not email_text:
            return render_template("index.html", error="You must enter your email text")
        if len(email_text) > 10000:
            return render_template("index.html", error="The email text is above the limit, please enter an email below 10000 ")
        prediction = predict_email(email_text)
        log_classification(email_text, prediction)

    return render_template("index.html", prediction=prediction)

LOG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'classified_log.csv')


def log_classification(email_text, prediction):
    headers = ["Timestamp", "Email Text", "Prediction", "Confidence Score", "Top Contributing Words"]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    label = prediction.get('label', 'N/A')
    confidence_score = round(float(prediction.get('confidence_score', 0)), 2)
    top_words = prediction.get('top_contributing_words', [])
    top_contributing_words = ', '.join([w['word'] for w in top_words]) if isinstance(top_words, list) else 'N/A'
    entry = [timestamp, email_text.strip(), label, confidence_score, top_contributing_words]

    write_header = not os.path.isfile(LOG_PATH) or os.stat(LOG_PATH).st_size == 0

    try:
        with open(LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(headers)
            writer.writerow(entry)
    except Exception as e:
        print(f"[Logging Error] Failed to log classification:{e}")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/edit_users')
@login_required
@admin_required
def edit_users():
    users = User.query.all()
    return render_template('admin/edit_users.html', users=users)

@app.route('/update_user_role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role in ['user', 'admin']:
        user.role = new_role
        database.session.commit()
        flash(f"Updated role for {user.username} to '{new_role}'", 'success')
    else:
        flash("Invalid role selected.", 'danger')
    return redirect(url_for('edit_users'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash("You cannot delete your own account.", 'warning')
        return redirect(url_for('edit_users'))

    user = User.query.get_or_404(user_id)
    database.session.delete(user)
    database.session.commit()
    flash(f"User '{user.username}' has been deleted.", 'success')
    return redirect(url_for('edit_users'))


@app.route('/edit/<timestamp>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_log(timestamp):
    entries = []
    updated_score = None
    updated_prediction = None
    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        headers = reader[0]
        entries = reader[1:]

    entry = next((row for row in entries if row[0] == timestamp), None)

    if not entry:
        flash("This entry could not be found.", "warning")
        return redirect(url_for('classification_log'))

    if request.method == 'POST':
        email_text = request.form.get("email_text")
        action = request.form.get("action")

        if action == "Recheck":
            result = predict_email(email_text)
            prediction_label = result['label']
            score = result['confidence_score']
            updated_score = round(float(score), 2)
            updated_prediction = prediction_label
            return render_template('admin/edit_log.html', entry=entry, prediction=updated_prediction, score=updated_score, email_text= email_text)
        elif action == "Save":
            print('SAVING')
            new_prediction = request.form.get("prediction")
            updated_entries = []
            for row in entries:
                if row[0] == timestamp:
                    new_label = request.form.get("prediction")
                    score = entry[3]
                    top_contributing_words = entry[4]
                    updated_entries.append([timestamp, email_text.strip(), new_label, score, top_contributing_words])
                else:
                    updated_entries.append(row)

            with open(LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(updated_entries)
            flash("Log edited successfully!", "success")
            return redirect(url_for('classification_log'))



    return render_template('admin/edit_log.html', entry=entry)


@app.route('/delete/<timestamp>', methods=['POST'])
@login_required
@admin_required
def delete_log(timestamp):
    entries = []
    deletedFlag = False
    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        reader = (csv.reader(f))
        headers = next(reader)
        rows = list(reader)
        for entry in rows:
            print("entry: ", entry)
            print(f"Comparing: entry[0]={entry[0]!r} vs timestamp={timestamp!r}")
            if entry[0].strip() != timestamp.strip():
                entries.append(entry)
            else:
                deletedFlag = True
    with open(LOG_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(entries)
    if deletedFlag:

        flash("Entry was deleted successfully!", "success")
    else:
        flash("This entry was not found.", "warning")
    return redirect(url_for('classification_log'))



@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@app.route('/classification_log.html')
@login_required
@admin_required
def classification_log():
    log_entries = []
    log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'classified_log.csv')
    headers = ["Timestamp", "Email Text", "Prediction", "Confidence Score", "Top Contributing Words"]

    q = request.args.get('q', '').lower();
    if os.path.exists(log_path):
        with open(log_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)
            for row in reader:
                timestamp = row[0]
                email_text = row[1]
                try:
                    label = row[2]
                    score = f"{float(row[3]):.2f}%"
                    top_contributing_words = row[4]
                    if q:
                        haystack = " ".join(row).lower()
                        if q not in haystack:
                            continue
                except Exception as e:
                    label = score = top_contributing_words = "Parsing Error with the File"
                log_entries.append([timestamp, email_text, label, score, top_contributing_words])


    return render_template('admin/classification_log.html', log_entries=log_entries, headers = ["Timestamp", "Email Text", "Prediction", "Confidence Score", "Top Contributing Words"], q=q)



if __name__ == '__main__':
    app.run()