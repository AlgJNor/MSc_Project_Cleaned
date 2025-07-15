from predict import predict_email

if __name__ == "__main__":
    email_text = input("Enter the email text:\n")
    result = predict_email(email_text)
    print(f"\nPrediction: {result}")
