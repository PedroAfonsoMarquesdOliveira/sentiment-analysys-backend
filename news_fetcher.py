import requests
from dotenv import load_dotenv
import os
import feedparser
from newspaper import Article

from schemas import BankRequest

load_dotenv()
def fetch_news(request: BankRequest):
    API_KEY = os.getenv("NEWS_API_KEY")
    if not API_KEY:
        raise ValueError("NEWS_API_KEY not found in environment variables.")
    url = f"https://newsapi.org/v2/everything?q={request.bank_name}&language={request.language}&apiKey={API_KEY}"
    response = requests.get(url)
    return response.json().get("articles", [])


# def fetch_serper_news(query: str):
#     url = "https://google.serper.dev/search"
#     headers = {
#         "X-API-KEY": os.getenv("SERPER_API_KEY"),
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "q": query,
#         "gl": "us",
#         "hl": "en"
#     }
#
#     response = requests.post(url, json=payload, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         # Extract news or organic results depending on your use case
#         return data.get("news", [])  # or data.get("organic", [])
#     else:
#         print("Serper API error:", response.status_code, response.text)
#         return []



#mais lento
def fetch_rss_articles(query: str):
    feed_url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(feed_url)
    print(feed)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
        })
    return articles



def extract_article_text(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return ""


