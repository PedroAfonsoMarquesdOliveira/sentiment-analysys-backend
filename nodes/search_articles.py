import requests

from news_fetcher import get_articles


def search_articles_node(state):
    try:
        articles = get_articles(state.bank_name, state.language, state.limit)
        print("Found" + str(len(articles)) + " articles")
        return {**state.dict(), "articles": articles, "error": None}
    except requests.HTTPError as e:
        return {**state.dict(), "articles": None, "error": f"HTTP Error: {e.response.status_code}, {e.response.text}"}
    except Exception as e:
        return {**state.dict(), "articles": None, "error": f"Unexpected error: {str(e)}"}
