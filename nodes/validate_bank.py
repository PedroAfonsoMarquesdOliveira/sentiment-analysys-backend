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


def validate_bank_node(state):
    bank = state.bank_name
    prompt = f"Is '{bank}' the name of a real bank? Answer yes or no."
    answer = llm.invoke(prompt).content.lower()
    if "yes" not in answer:
        print(bank + " is not a bank")
        return {"error": f"'{bank}' is not recognized as a real bank."}
    return state


def has_error(state):
    return "error" if state.error else "success"
