from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

# Tell Presidio to use en_core_web_sm (already installed!)
configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "en", "model_name": "en_core_web_sm"}
    ],
}
# Create the NLP engine provider and engine 
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
# Create the analyzer and anonymizer engines
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

text = 'Hi I am John Smith. My number is 9876543210 and email is john@gmail.com'
#Only detect these specific PII types
results = analyzer.analyze(text=text, language='en', entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD", "LOCATION"])
print('DETECTED PII:')
for r in results:
    print(f'  {r.entity_type}: {text[r.start:r.end]}')

anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
print('\nREDACTED TEXT:')
print(anonymized.text)
print("\n--- TESTING ALL PII TYPES ---\n")

tests = [
    'My name is John and card is 4111 1111 1111 1111',
    'Address is 123 Main Street, New York',
    'Date of birth: 15th March 1990',
    'My SSN is 123-45-6789',
    'Call back at +1-800-555-0199 before 5pm'
]

for t in tests:
    r = analyzer.analyze(
        text=t,
        language='en',
        entities=["PERSON", "PHONE_NUMBER",
                  "EMAIL_ADDRESS", "CREDIT_CARD",
                  "LOCATION"]
    )
    a = anonymizer.anonymize(text=t, analyzer_results=r)
    print(f"INPUT:    {t}")
    print(f"REDACTED: {a.text}")
    print()