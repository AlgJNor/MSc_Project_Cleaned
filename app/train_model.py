import pandas as pd
import glob
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

# 1. Load and merge datasets
folder_path = 'Phishing Dataset'
files = glob.glob(os.path.join(folder_path, '*.csv'))  # Replace 'data/' with your folder

df_list = [pd.read_csv(file, encoding='utf-8') for file in files]
df = pd.concat(df_list, ignore_index=True)

# 2. Clean data
df.drop_duplicates(inplace=True)
df.dropna(subset=['subject', 'body', 'label'], inplace=True)

# 3. Combine subject and body
df['text'] = df['subject'].fillna('') + ' ' + df['body'].fillna('')

# 4. Preprocess text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)  # remove punctuation
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    return text.strip()

df['text'] = df['text'].apply(clean_text)

# 5. Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])

# 6. Labels
y = df['label']

# 7. Train model
model = LogisticRegression()
model.fit(X, y)

# 8. Save model and vectorizer
with open("phishing_detector.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved.")
