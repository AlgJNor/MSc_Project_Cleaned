import pickle
import os, sys
from app.pre_process import clean_text

def predict_email(email_text):
    # Load model
    phishing_model_path = os.path.join(os.path.dirname(__file__), 'phishing_detector.pkl')
    with open(phishing_model_path, "rb") as f:
        model = pickle.load(f)

    # Load vectorizer
    vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    # Preprocess and vectorize
    cleaned = clean_text(email_text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)

    return "Phishing" if prediction[0] == 1 else "Not Phishing"
