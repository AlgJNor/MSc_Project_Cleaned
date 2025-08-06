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
    prediction = model.predict_proba(vector)[0][1]
    confidence_score = prediction * 100

    if prediction >= 0.7:
        label = "Phishing"
    elif prediction <= 0.30:
        label = "Not Phishing"
    else:
        label = "Uncertain"

    get_feature_names = vectorizer.get_feature_names_out()
    word_weights = vector.toarray()[0]
    top_indices = word_weights.argsort()[::-1][:5]
    total_weight = sum(word_weights)
    top_contributing_words = [
        {"word": get_feature_names[i], "weight": round((word_weights[i] / total_weight) * 100, 2)}
        for i in top_indices if word_weights[i] > 0
    ]


    return {
       "label": label,
        "confidence_score": f"{confidence_score:.2f}",
        "top_contributing_words": top_contributing_words
    }
