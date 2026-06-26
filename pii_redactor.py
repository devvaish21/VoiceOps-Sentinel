import re
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

# Configuration using spaCy as the NLP engine with the English model
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en",
                "model_name": "en_core_web_sm"}],
}

# Initialize the NLP engine with the specified configuration
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
# Initialize the Presidio Analyzer and Anonymizer engines for PII detection and redaction
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

def fix_spoken_email(text):
    return re.sub(
        r'(\w+)\.(\w+)\.(com|in|org|net)',
        r'\1@\2.\3',
        text
    )
# Function to redact PII from the text using Presidio
def redact_pii(text: str) -> str:
    # preprocess text to fix spoken email addresses
    text = fix_spoken_email(text)
    if not text or not text.strip():
        return text
    # Analyze the text for PII entities
    results = analyzer.analyze(
        text=text,
        language='en',
        entities=["PERSON", "PHONE_NUMBER",
                  "EMAIL_ADDRESS", "CREDIT_CARD",
                  "LOCATION"]
    )
    if not results:
        return text
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )
    return anonymized.text

# Test the redact_pii function with a sample input
if __name__ == "__main__":
    # Define a sample test string containing PII
    test = "Agent: Calling about John Smith. Card is 4111111111111111"
    print("ORIGINAL:", test)
    print("REDACTED:", redact_pii(test))