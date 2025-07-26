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
        if not email_text:
            return render_template("index.html", error="You must enter your email text")
        if len(email_text) > 10000:
            return render_template("index.html", error="The email text is above the limit, please enter an email below 10000 ")
        prediction = predict_email(email_text)
    return render_template("index.html", prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)