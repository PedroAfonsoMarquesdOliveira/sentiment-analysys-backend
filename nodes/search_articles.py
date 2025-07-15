
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
    print(f"Calling GNews: {url} with params: {params}")
    try:
        print(f"Calling GNews: {url} with params: {params}")
        response = requests.get(url, params=params)

        # Raise HTTPError for non-200 responses
        response.raise_for_status()

        # Check if content is empty to avoid JSONDecodeError
        if not response.content.strip():
            return {**state.dict(), "articles": None, "error": "GNews returned empty response."}

        articles = response.json().get("articles", [])
        return {**state.dict(), "articles": articles, "error": None}

    except requests.exceptions.HTTPError as e:
        return {**state.dict(), "articles": None, "error": f"HTTP Error {e.response.status_code}: {e.response.text}"}

    except requests.exceptions.JSONDecodeError as e:
        return {**state.dict(), "articles": None, "error": f"Invalid JSON from GNews: {str(e)}"}

    except Exception as e:
        return {**state.dict(), "articles": None, "error": f"Unexpected error: {str(e)}"}


