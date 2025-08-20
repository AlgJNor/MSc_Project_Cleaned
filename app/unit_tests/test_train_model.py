import os
from pathlib import Path
import pandas as pd
import importlib
import shutil

def ensure_dataset_next_to_module(test_file: Path):
    """
    Creates a sample 'Phishing Dataset' next to the train_model.py script
    so the script has data to process when imported.
    """
    app_dir = test_file.resolve().parents[1]
    dataset_dir = app_dir / "Phishing Dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)

    data1 = pd.DataFrame(
        {
            "subject": [
                "Win $$$ NOW!!!",
                "This is not spam, visit now",
                "Update your Account http://bad.url",
                None,
            ],
            "body": [
                "Click http://phish.me to claim prize",
                "Seriously, NOT spam — limited offer",
                "Please login at https://evil.co to continue",
                "orphan row",
            ],
            "label": [1, 0, 1, 0],
        }
    )
    data2 = pd.DataFrame(
        {
            "subject": [
                "This is not spam, visit now",
                "Monthly newsletter",
            ],
            "body": [
                "Seriously, NOT spam — limited offer",
                "Your monthly updates are here.",
            ],
            "label": [0, 0],
        }
    )

    data1.to_csv(dataset_dir / "part1.csv", index=False)
    data2.to_csv(dataset_dir / "part2.csv", index=False)

    return app_dir, dataset_dir


def clean_artifacts(app_dir: Path):
    """
    Removes any model and vectorizer files so that repeated test runs
    start with a clean state.
    """
    for name in ("phishing_detector.pkl", "vectorizer.pkl"):
        p = app_dir / name
        if p.exists():
            p.unlink()


def test_script_end_to_end(monkeypatch):
    """
    Validates that running the training script produces cleaned data,
    correct vectorizer settings, a trained model, and saved artifacts.
    """
    test_file = Path(__file__)
    app_dir, dataset_dir = ensure_dataset_next_to_module(test_file)
    clean_artifacts(app_dir)

    if "app.train_model" in list(importlib.sys.modules):
        del importlib.sys.modules["app.train_model"]
    train_model = importlib.import_module("app.train_model")

    s = "This is NOT spam! Visit http://example.com NOW 123 !!!"
    cleaned = train_model.clean_text(s)
    assert "not_spam" in cleaned
    assert "http" not in cleaned and "example.com" not in cleaned
    assert "123" not in cleaned
    assert cleaned == cleaned.strip()

    df = train_model.df
    assert len(df) == 4
    assert "text" in df.columns
    assert df["text"].str.len().min() > 0

    vect = train_model.vectorizer
    assert vect.stop_words == "english"
    assert vect.ngram_range == (1, 2)
    assert vect.min_df == 3
    assert vect.max_df == 0.85

    X = train_model.X
    y = train_model.y
    assert X.shape[0] == len(df)
    assert X.shape[1] > 0
    assert len(y) == len(df)

    model = train_model.model
    assert hasattr(model, "classes_")
    assert set(model.classes_) <= {0, 1}

    model_path = app_dir / "phishing_detector.pkl"
    vec_path = app_dir / "vectorizer.pkl"
    assert model_path.exists()
    assert vec_path.exists()

    clean_artifacts(app_dir)


def test_clean_text_edge_cases():
    """
    Checks that clean_text handles unusual inputs, spacing, punctuation,
    and the joining of 'not spam' into a single token.
    """
    from app import train_model

    assert train_model.clean_text(None) == ""
    assert train_model.clean_text("123") == ""
    s = "  Hello,   world!!!  "
    out = train_model.clean_text(s)
    assert out == "hello world"
    assert "not_spam" in train_model.clean_text("This is not spam")