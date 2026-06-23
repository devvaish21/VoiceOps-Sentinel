import spacy
nlp = spacy.load('en_core_web_sm')

text = 'Hi, I am John Smith. My number is 9876543210 and email is john@gmail.com'
doc = nlp(text)

for ent in doc.ents:
    print(f'Found: {ent.text}  →  Type: {ent.label_}')