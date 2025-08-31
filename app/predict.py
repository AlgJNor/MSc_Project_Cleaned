import pickle
import os, sys
from app.pre_process import clean_text

def predict_email(email_text): #Takes the raw email text and returns a prediction result
    # Load model
    phishing_model_path = os.path.join(os.path.dirname(__file__), 'phishing_detector.pkl') #Builds path and unpickles model
    with open(phishing_model_path, "rb") as f: #Loads model
        model = pickle.load(f)

    # Load vectorizer
    vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl') #Builds path and unpickles vectorizer
    with open(vectorizer_path, "rb") as f: #Loads vectorizer
        vectorizer = pickle.load(f)

    # Preprocess and vectorize
    cleaned = clean_text(email_text) #applies normalization (lowercasing, stripping HTML, etc.)
    vector = vectorizer.transform([cleaned]) #converts to a sparse feature vector for the model
    prediction = model.predict_proba(vector)[0][1] #probability of positive class
    confidence_score = prediction * 100

    if prediction >= 0.7: #phishing if >= 70%
        label = "Phishing"
    elif prediction <= 0.30: # not phishing if <= 30%
        label = "Not Phishing"
    else:
        label = "Uncertain"

    get_feature_names = vectorizer.get_feature_names_out() # gets a list of all feature names for the email
    word_weights = vector.toarray()[0] # gives TF-IDF weights for every word in the email
    top_indices = word_weights.argsort()[::-1][:5] # top 5 weighted words in the email
    total_weight = sum(word_weights) # compute sum of all weights
    top_contributing_words = [ # builds a list of dicts for: the top words and their weights
        {"word": get_feature_names[i], "weight": round((word_weights[i] / total_weight) * 100, 2)}
        for i in top_indices if word_weights[i] > 0
    ]


    return {
       "label": label,
        "confidence_score": f"{confidence_score:.2f}",
        "top_contributing_words": top_contributing_words
    }
