import pickle
from pre_process import clean_text

def predict_email(email_text):
    # Load model
    with open("phishing_detector.pkl", "rb") as f:
        model = pickle.load(f)

    # Load vectorizer
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    # Preprocess and vectorize
    cleaned = clean_text(email_text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)

    return "Phishing" if prediction[0] == 1 else "Not Phishing"
