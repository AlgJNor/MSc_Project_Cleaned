import pandas as pd
import glob
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt

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
    text = re.sub(r"\bnot\s+(\w+)", r"not_\1", text) #Join 'not' with next token
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)  # remove punctuation
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    return text.strip()

df['text'] = df['text'].apply(clean_text)

# 5. Vectorization
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df=3, max_df=0.85, max_features=10000)
X = vectorizer.fit_transform(df['text'])

print(X.shape)

# 6. Labels
y = df['label']

# 7. Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 8. Train the model on th training data
model = LogisticRegression()
model.fit(X_train, y_train)

# 9. Evaluate the model on the test data
y_prediction = model.predict(X_test)
accuracy = accuracy_score(y_test, y_prediction)
precision = precision_score(y_test, y_prediction)
recall = recall_score(y_test, y_prediction)
f1 = f1_score(y_test, y_prediction)

print(f"\nEvaluation on Model:")
print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1 Score: {f1:.2%}")
print("\nDetailed Report of the Model:\n", classification_report(y_test, y_prediction))

y_probas = model.predict_proba(X_test)[:,1]

print(confusion_matrix(y_test, y_prediction))

fpr, tpr, _ = roc_curve(y_test, y_probas)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], '--')
plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic'); plt.legend(loc='lower right')
plt.show()

# 10. Save model and vectorizer
with open("app/phishing_detector.pkl", "wb") as f:
    pickle.dump(model, f)

with open("app/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved.")
