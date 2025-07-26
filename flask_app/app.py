from flask import Flask, request, render_template
import sys
import os
from app.predict import predict_email

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        email_text = request.form.get("email_text")
        if email_text:
            prediction = predict_email(email_text)
    return render_template("index.html", prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)