import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, save_results, read_sentiments, save_results_llm
from graph import build_graph, State, build_graph_serper_api
from news_fetcher import fetch_bank_news
from nodes.sentiment_analysis import analyze_articles, analyze_bank_news_v2
from schemas import BankRequest

app = FastAPI()


# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
        return db
    finally:
        db.close()


port = int(os.environ.get("PORT", 8000))  # default fallback to 8000

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=port, reload=True)

graph = build_graph()
graph_serper_api = build_graph_serper_api()

# CORS for React frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local dev
        "https://sentiment-analysys-frontend.vercel.app",  # Vercel production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API is running!"}


def get_or_fetch_and_save(
        bank_name: str,
        db: Session,
        fetch_fn,
        limit: int = None,
        use_llm_save: bool = False,
):
    existing = read_sentiments(bank_name, db)
    if existing and (limit is None or len(existing) >= limit):
        print("enough existing in database")
        return existing[:limit] if limit else existing

    # fetch new results
    results = fetch_fn()

    # Choose save function based on flag
    if use_llm_save:
        save_results_llm(bank_name, db, results)
    else:
        save_results(bank_name, db, results)

    return results



@app.post("/analyze/")
def analyze_sentiment(request: BankRequest, db: Session = Depends(get_db)):
    return get_or_fetch_and_save(
        bank_name=request.bank_name,
        db=db,
        limit=request.limit,
        fetch_fn=lambda: analyze_articles(fetch_bank_news(request))
    )


@app.post("/analyze_llm/")
def analyze(request: State, db: Session = Depends(get_db)):
    def fetch():
        result = graph.invoke({"bank_name": request.bank_name, "language": request.language, "limit": request.limit})
        if "error" in result and result["error"]:
            raise ValueError(result["error"])
        return result.get("results")

    try:
        return get_or_fetch_and_save(
            bank_name=request.bank_name,
            db=db,
            fetch_fn=fetch,
            limit=request.limit,
            use_llm_save=True
        )
    except ValueError as e:
        return {"error": str(e)}


@app.post("/analyze_llm_serper/")
def analyze(request: State, db: Session = Depends(get_db)):
    def fetch():
        result = graph_serper_api.invoke(
            {"bank_name": request.bank_name, "language": request.language, "limit": request.limit})
        if "error" in result and result["error"]:
            raise ValueError(result["error"])
        return result.get("results")

    try:
        return get_or_fetch_and_save(
            bank_name=request.bank_name,
            db=db,
            fetch_fn=fetch,
            limit=request.limit,
            use_llm_save=True
        )
    except ValueError as e:
        return {"error": str(e)}


@app.post("/analyze_v2/")
def analyze_sentiment_v2(request: BankRequest, db: Session = Depends(get_db)):
    return get_or_fetch_and_save(
        bank_name=request.bank_name,
        db=db,
        fetch_fn=lambda: analyze_bank_news_v2(request),
        limit=request.limit
    )
