from predict import predict_email

if __name__ == "__main__":
    print("Enter the email text below:")
    print("When done, type 'END' on a new line and press Enter.\n")

    lines = []
    while True:
        line  = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    email_text = "\n".join(lines)

    result = predict_email(email_text)
    print(f"\nPrediction: {result}")
