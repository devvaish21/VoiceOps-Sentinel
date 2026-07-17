from transformers import pipeline

classifier = pipeline("sentiment-analysis")


def analyze_sentiment(text: str):
    result = classifier(text[:512])

    return {
        "label": result[0]["label"],
        "score": round(result[0]["score"], 2)
    }