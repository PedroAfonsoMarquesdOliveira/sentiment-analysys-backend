from transformers import pipeline

from news_fetcher import fetch_rss_articles, extract_article_text

sentiment_model = pipeline("sentiment-analysis")

def analyze_articles(articles):
    results = []
    for article in articles:
        title = article.get("title") or ""
        desc = article.get("description") or ""
        content = (title + " " + desc)[:512]
        sentiment = sentiment_model(content)[0]

        results.append({
            "title": title,
            "url": article.get("url"),
            "sentiment": sentiment["label"],
            "score": sentiment['score']
        })
    return results


def analyze_bank_news_v2(bank_name: str):
    articles = fetch_rss_articles(bank_name)
    results = []

    for article in articles:
        full_text = extract_article_text(article["link"])
        content = (article["title"] + " " + full_text)[:512]
        sentiment = sentiment_model(content)[0]

        results.append({
            "title": article["title"],
            "url": article["link"],
            "sentiment": sentiment["label"],
            "score": sentiment["score"]
        })

    return results

