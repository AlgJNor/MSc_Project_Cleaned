# Phishing Deetection Application Backend

This is the backend service of the phishing email detection system.
It handles **Ddata preprocessing, feature extraction, model training, and predictions** using Maching Learning

## Features

- Load and clean phishing email datasets (CSV format)
- Preprocess text (punctuation removal, lowercasing, tokenization)
- Feature extraction via **TF-IDF Vectorizer**.
- Train a **Logistic Regression Classifier**.
- Save and Load the trained model (`phishing_detector.pkl`) and vectorizer (`vectorizer.pkl`).
- Unit tests written for the training and prediction pipeline

## Project Structure

```bash
app/
├── Phishing Dataset/ #Email datasets (in csv)
│── unit_tests/ #Unit tests for the detection
│   └── init.py
│   └── test_clean_text.py
│   └── test_predict_email.py
│   └── test_train_model.py
├── main.py
├── phishing_detector.pkl
├── pre_process.py
├── predict.py
├── README.md
├── requirements.txt
├── train_model.py
├── vectorizer.pkl

````

## Installation

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to use

### Train the model
```bash
    python train_model.py
```
### Run the prediction

Please read the `flask_app/README.md` to run the Flask App
### Run Tests

```bash
pytest unit_tests/
```
