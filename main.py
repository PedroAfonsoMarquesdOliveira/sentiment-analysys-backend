from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from graph import build_graph, State, build_graph_serper_api
from news_fetcher import fetch_news, fetch_bank_news
from nodes.sentiment_analysis import analyze_articles, analyze_bank_news_v2
from schemas import BankRequest

app = FastAPI()



port = int(os.environ.get("PORT", 8000))  # default fallback to 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=port, reload=True)

graph = build_graph()
graph_serper_api=build_graph_serper_api()
# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API is running!"}



@app.post("/analyze/")
def analyze_sentiment(request: BankRequest):
    articles = fetch_bank_news(request)
    results = analyze_articles(articles)
    return results


@app.post("/analyze_llm/")
def analyze(request: State):
    print(request)
    result = graph.invoke({"bank_name": request.bank_name, "language": request.language})
    if "error" in result and result["error"]:
        return {"error": result["error"]}
    return result.get("results")


@app.post("/analyze_llm_serper/")
def analyze(request: State):
    result = graph.invoke({"bank_name": request.bank_name, "language": request.language})
    if "error" in result and result["error"]:
        return {"error": result["error"]}
    return result.get("results")


@app.post("/analyze_v2/")
def analyze_sentiment_v2(request: BankRequest):
    results = analyze_bank_news_v2(request.bank_name)
    return results
