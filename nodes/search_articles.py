
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
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.HTTPError as e:
        return [{"error": f"HTTP Error: {e.response.status_code}, {e.response.text}"}]
    except Exception as e:
        return [{"error": f"Error fetching news: {str(e)}"}]

