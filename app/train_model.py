import pandas as pd
import glob
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

# 1. Load and merge datasets
folder_path = os.path.join(os.path.dirname(__file__), 'Phishing Dataset')
files = glob.glob(os.path.join(folder_path, '*.csv'))  # Replace 'data/' with your folder
df_list = []
for file in files:
    try:
        df = pd.read_csv(file, encoding='utf-8')
        df_list.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")
df = pd.concat(df_list, ignore_index=True)

# 2. Clean data
df.drop_duplicates(inplace=True)
df.dropna(subset=['subject', 'body', 'label'], inplace=True)

# 3. Combine subject and body
df['text'] = df['subject'].fillna('') + ' ' + df['body'].fillna('')

# 4. Preprocess text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\bnot\s+(\w+)", r"not_\1", text)
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)  # remove punctuation
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    return text.strip()

df['text'] = df['text'].apply(clean_text)

# 5. Vectorization
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df=3, max_df=0.85)
X = vectorizer.fit_transform(df['text'])

# 6. Labels
y = df['label']

# 7. Train model
model = LogisticRegression()
model.fit(X, y)

# 8. Save model and vectorizer
with open("app/phishing_detector.pkl", "wb") as f:
    pickle.dump(model, f)

with open("app/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved.")
