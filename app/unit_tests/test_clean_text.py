import pytest

from app.pre_process import clean_text

def test_email_replacement():
    text = "Please contact me at example@example.com"
    result = clean_text(text)
    assert "emailaddress" in result
    assert "example" not in result

def test_url_replacement():
    text = "visit https://example.com or https://test.co.uk"
    result = clean_text(text)
    assert "url" in result
    assert "https://" not in result

def test_white_space_removal():
    text = "Example email body    spaces\tand\nnewlines"
    result = clean_text(text)
    assert "  " not in result
    assert "\n" not in result
    assert "\t" not in result

def test_lowercase():
    text = "This TEXT shouldbe In LoweCASE"
    result = clean_text(text)
    assert result == result.lower()

def test_special_characters_removal():
    text = "Win £5000 now!!! Click here"
    result = clean_text(text)
    assert "£" not in result
    assert "!!!" not in result
    assert "now" in result



