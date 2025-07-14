
from transformers import pipeline
sentiment_model = pipeline("sentiment-analysis")



def sentiment_node(state):
    articles = state.articles
    results = []
    for article in articles:
        if not article.title or not article.content:
            continue  # Skip this article
        text = (article.title or "") + " " + (article.content or "")
        text = text.strip()[:512]
        sentiment = sentiment_model(text)[0]

        results.append({
            "title": article.title,
            "url": article.url,
            "sentiment": sentiment["label"],
            "score": sentiment["score"]
        })

    return {**state.dict(), "results": results}
