import wikipedia


def fetch_wikipedia_summary(topic: str) -> str:
    try:
        return wikipedia.summary(topic, sentences=3)
    except Exception as e:
        return f"Wikipedia error: {e}"
