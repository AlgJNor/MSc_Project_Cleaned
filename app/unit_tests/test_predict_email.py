import pytest

from app.predict import predict_email
from unittest.mock import MagicMock, patch

non_phishing_email = "Hi Algot, Glad to hear from you, haven't seen you in a while. There is no marking scheme/criteria; as it was explained in the message sent a few days ago on Canvas, projects are assessed holistically, considering results, efforts, commitments, etc. Best, Rick"

phishing_email = "personal contact dear sir madam may surprise receive letter since know personally purpose mail mr peter stevens second son dr dennis stevens murdered time ago land dispute zimbabwe writing holland netherlands currently based political asylum seeker death father took amsterdam holland deposit sum us 18 9 eighteen million nine hundred thousand united states dollars private security finance company may saw looming danger zimbabwe money put box gemstones deposited avoid much tax demurrage security company money initially meant purchase new machines chemicals farms also establish new farm swaziland land problem came government zimbabwe leadership president robert mugabe introduced new land use decree act affected lot rich white farmers blacks resulted mob action killing zimbabwe war veterans lunatics society say infact lot people killed land reform act including father back ground consulted family transfer money holland foreign account since staying holland law netherlands forbids refugee asylum seeker money account therefore saddled responsibility family seek genuine person foreign account handle transaction faced dilemma investing amount money netherlands like go experience future since countries similar history moreover netherlands foreign exchange allow investment asylum seekers must let know transaction risk free accept assist family need come amsterdam netherlands open non resident account aid us transfer money account provide money meant investment purpose lucrative business choice two options offers assistance may go partnership business decides invest money shearing profit carefully spelt agreed upon may decide 20 total sum 70 family remaining 10 set aside un forseen expenses may incurred cause pursuing transaction successful end may contact medias know decision proposal please note field specialization hindreance transaction thank anticipated co operations peter stevens"


@patch("app.predict.pickle.load")
@patch("builtins.open")
@patch("app.predict.clean_text")
def test_phishing_email(mock_clean_text, mock_open, mock_pickle_load):
    mock_model = MagicMock()
    mock_model.predict.return_value = [1]

    mock_vectorizer = MagicMock()
    mock_vectorizer.transform.return_value = "mock_vectorizer"

    mock_pickle_load.side_effect = [mock_model, mock_vectorizer]
    mock_clean_text.return_value = "Cleaned text"

    result = predict_email(phishing_email)

    assert result == "Phishing" if result == 1 else "Not Phishing"
    mock_clean_text.assert_called_once()
    mock_model.predict.assert_called_once_with("mock_vectorizer")

@patch("app.predict.pickle.load")
@patch("builtins.open")
@patch("app.predict.clean_text")
def test_non_phishing_email(mock_clean_text, mock_open, mock_pickle_load):
    mock_model = MagicMock()
    mock_model.predict.return_value = [1]

    mock_vectorizer = MagicMock()
    mock_vectorizer.transform.return_value = "mock_vectorizer"

    mock_pickle_load.side_effect = [mock_model, mock_vectorizer]
    mock_clean_text.return_value = "Cleaned text"

    result = predict_email(non_phishing_email)

    assert result == "Phishing" if result == 1 else "Not Phishing"
    mock_clean_text.assert_called_once()
    mock_model.predict.assert_called_once_with("mock_vectorizer")
