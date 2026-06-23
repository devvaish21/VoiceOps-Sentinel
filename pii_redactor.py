from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en",
                "model_name": "en_core_web_sm"}],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

def redact_pii(text: str) -> str:
    if not text or not text.strip():
        return text
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

# Test
if __name__ == "__main__":
    test = "Agent: Calling about John Smith. Card is 4111111111111111"
    print("ORIGINAL:", test)
    print("REDACTED:", redact_pii(test))