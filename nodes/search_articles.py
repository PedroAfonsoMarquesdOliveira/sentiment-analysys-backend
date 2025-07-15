
import requests
import os


def search_articles_node(state):
    API_KEY = os.getenv("GNEWS_API_KEY")
    if not API_KEY:
        raise ValueError("GNEWS_API_KEY not found in environment variables.")
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": state.bank_name,
        "token": API_KEY,
        "lang": "en",
        "max": state.limit
    }

    try:
        response = requests.get(url, params=params)
        articles = response.json().get("articles", [])
        return {**state.dict(), "articles": articles}
    except requests.HTTPError as e:
        return {**state.dict(), "articles": None, "error": f"HTTP Error: {e.response.status_code}, {e.response.text}"}
    except Exception as e:
        return {**state.dict(), "articles": None, "error": f"Error fetching news: {str(e)}"}

