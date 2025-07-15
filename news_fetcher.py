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

    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": request.bank_name,
        "apiKey": API_KEY,
        "pageSize": request.limit
    }
    if request.language != "all":
        params["language"] = request.language

    response = requests.get(base_url, params=params)

    # Check for HTTP errors
    try:
        response.raise_for_status()  # Raises an error for 4xx/5xx codes
        return response.json().get("articles", [])
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}, Status Code: {response.status_code}, Body: {response.text}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}, Body: {response.text}")

    # Fallback: return empty list if error happens
    return []


def fetch_bank_news(request: BankRequest):
    API_KEY = os.getenv("GNEWS_API_KEY")
    if not API_KEY:
        raise ValueError("GNEWS_API_KEY not found in environment variables.")
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": request.bank_name,
        "token": API_KEY,
        "lang": "en",
        "max": request.limit
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.HTTPError as e:
        return [{"error": f"HTTP Error: {e.response.status_code}, {e.response.text}"}]
    except Exception as e:
        return [{"error": f"Error fetching news: {str(e)}"}]


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
def fetch_rss_articles(request: BankRequest):
    feed_url = f"https://news.google.com/rss/search?q={request.bank_name}"
    feed = feedparser.parse(feed_url)
    # Only extract what's needed
    return [
        {
            "title": entry.title,
            "link": entry.link,
        }
        for entry in feed.entries[:request.limit]
    ]



def extract_article_text(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return ""


