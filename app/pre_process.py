import re
import string

def clean_text(text):
    print("TEXT", text)
    text = text.lower()

    # replace URLs and emails
    text = re.sub(r"\S+@\S+", " emailaddress ", text)
    text = re.sub(r"http\S+|www\S+", " url ", text)

    text = re.sub(r"[^\w\s.@]", " ", text) # keeps dots for domains

    # normalise whitespace
    text = re.sub(r"\s+", " ", text).strip()

    print("New cleaned text:\n", text)
    return text
