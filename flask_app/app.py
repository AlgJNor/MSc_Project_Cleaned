import csv

from flask import Flask, request, render_template
from datetime import datetime
import sys
import os
os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app','predict.py'))
from app.predict import predict_email

app = Flask(__name__)

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

LOG_PATH = 'classified_log.csv'


def log_classification(email_text, prediction):
    headers = ["Timestamp", "Email Text", "Prediction"]
    entry = [datetime.now().isoformat(), email_text.strip(), prediction]

    write_header = not os.path.isfile(LOG_PATH) or os.stat(LOG_PATH).st_size == 0

    try:
        with open(LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(headers)
            writer.writerow(entry)
    except Exception as e:
        print(f"[Logging Error] Failed to log classification: {e}")

if __name__ == '__main__':
    app.run(debug=True)