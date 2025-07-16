import requests
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="mistral-medium-latest",  # or mistral-small, mistral-medium
    temperature=0,
    openai_api_base="https://api.mistral.ai/v1",
    openai_api_key=os.environ["OPENAI_API_KEY"])


def is_real_bank_serper_and_llm(state):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }
    payload = {
        "q": state.bank_name,
    }
    if state.language != "all":
        payload["hl"] = state.language

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print("Serper API error:", response.status_code, response.text)
        return False

    data = response.json()
    results = data.get("organic", []) + data.get("news", [])

    context = ""
    for res in results[:5]:  # Use top 5 results
        title = res.get("title", "")
        snippet = res.get("snippet", "")
        context += f"Title: {title}\nSnippet: {snippet}\n\n"

    prompt = (
        f"Given these search results, is '{state.bank_name}' a real bank or financial institution? "
        "Answer 'Yes' or 'No'.\n\n"
        f"{context}"
    )
    response = llm.invoke(prompt).content.strip().lower()
    if "yes" not in response:
        print(state.bank_name + " is not a bank")
        return {"error": f"'{state.bank_name}' is not recognized as a real bank."}
    return state
