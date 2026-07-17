import spacy

nlp = spacy.load("en_core_web_sm")


KEYWORDS = [
    "call",
    "send",
    "email",
    "share",
    "schedule",
    "meet",
    "review",
    "submit",
    "update",
    "complete"
]


def extract_action_items(text: str):
    doc = nlp(text)

    actions = []

    for sent in doc.sents:
        sentence = sent.text.strip()

        if any(keyword in sentence.lower() for keyword in KEYWORDS):
            actions.append(sentence)

    return actions