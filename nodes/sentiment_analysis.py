from news_fetcher import fetch_rss_articles, extract_article_text
import os
from huggingface_hub import InferenceClient

from schemas import BankRequest

client = InferenceClient(
    provider="auto",
    api_key=os.environ["HF_TOKEN"],
)


def sentiment_node(state):
    articles = state.articles
    results = []
    for article in articles:
        if not article.title or not article.content:
            continue  # Skip this article
        text = (article.title or "") + " " + (article.content or "")
        text = text.strip()[:512]
        result = client.text_classification(
            text,
            model="tabularisai/multilingual-sentiment-analysis",
        )
        highest = max(result, key=lambda x: x['score'])
        results.append({
            "title": article.title,
            "url": article.url,
            "sentiment": highest["label"],
            "score": highest["score"]
        })

    return {**state.dict(), "results": results}


def analyze_articles(articles):
    results = []
    for article in articles:
        title = article.get("title") or ""
        desc = article.get("content") or ""
        if not title or not desc:
            continue  # Skip article if either field is missing or empty
        content = (title + " " + desc)[:512]
        result = client.text_classification(
            content,
            model="tabularisai/multilingual-sentiment-analysis",
        )
        highest = max(result, key=lambda x: x['score'])

        results.append({
            "title": title,
            "url": article.get("url"),
            "sentiment": highest["label"],
            "score": highest["score"]
        })
    return results


# muito lento
def analyze_bank_news_v2(request: BankRequest):
    articles = fetch_rss_articles(request)
    results = []

    for article in articles:
        full_text = extract_article_text(article["link"])
        content = (article["title"] + " " + full_text)[:512]
        result = client.text_classification(
            content,
            model="tabularisai/multilingual-sentiment-analysis",
        )
        highest = max(result, key=lambda x: x['score'])

        results.append({
            "title": article["title"],
            "url": article["link"],
            "sentiment": highest["label"],
            "score": highest["score"]
        })

    return results
