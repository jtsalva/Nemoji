from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def analyze_sentiment(text):
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    return sentiment.score
