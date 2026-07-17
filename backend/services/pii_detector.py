import re


def detect_pii(text: str):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)

    phones = re.findall(
        r'(?:\+91[- ]?)?[6-9]\d{9}',
        text
    )

    return {
        "emails": list(set(emails)),
        "phones": list(set(phones))
    }