
import requests
import os


def search_articles_node(state):
    bank = state.bank_name
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    url = f"https://newsapi.org/v2/everything?q={bank}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    return {**state.dict(), "articles": articles}

