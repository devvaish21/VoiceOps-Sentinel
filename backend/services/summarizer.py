from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)


def generate_summary(text: str):
    if len(text.split()) < 30:
        return text

    summary = summarizer(
        text,
        max_length=100,
        min_length=30,
        do_sample=False
    )

    return summary[0]["summary_text"]