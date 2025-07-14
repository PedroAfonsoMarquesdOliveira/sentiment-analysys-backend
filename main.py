from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from graph import build_graph, State, build_graph_serper_api
from news_fetcher import fetch_news
from schemas import BankRequest
from sentiment_analysis import analyze_articles, analyze_bank_news_v2

app = FastAPI()
graph = build_graph()
graph_serper_api=build_graph_serper_api()
# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/analyze/")
def analyze_sentiment(request: BankRequest):

    articles = fetch_news(request)
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
