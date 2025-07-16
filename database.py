from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()
from schemas import SentimentResult


# Your Pydantic model (input/output validation)
class SentimentResult_save(BaseModel):
    title: Optional[str]
    url: Optional[str]
    sentiment: str
    score: float
    name: str


# SQLAlchemy setup
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # local file named test.db
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# ) #for local

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Define the SQLAlchemy model
class SentimentResultDB(Base):
    __tablename__ = "sentiment_results"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    sentiment = Column(String)
    score = Column(Float)
    name = Column(String)
    language = Column(String)


# Create the tables
Base.metadata.create_all(bind=engine)


def read_sentiments(bank_name, language, db: Session):
    query = db.query(SentimentResultDB)
    if bank_name is None:
        query = query.filter(SentimentResultDB.name.is_(None))
    else:
        query = db.query(SentimentResultDB).filter(SentimentResultDB.name == bank_name)

    if language is None:
        query = query.filter(SentimentResultDB.language.is_(None))
    else:
        query = query.filter(SentimentResultDB.language == language)

    return query.all()

    results = query.all()
    return [
        SentimentResult(
            title=r.title,
            url=r.url,
            sentiment=r.sentiment,
            score=r.score,
            name=r.name
        )
        for r in results
    ]


def save_results(bank_name: str, language: str, db: Session, results: list):
    for res in results:
        exists = db.query(SentimentResultDB).filter(
            SentimentResultDB.url == res.get("url")
        ).first()

        if not exists:
            db_result = SentimentResultDB(
                title=res.get("title"),
                url=res.get("url"),
                sentiment=res.get("sentiment"),
                score=res.get("score"),
                name=bank_name,
                language=language
            )
            db.add(db_result)

    db.commit()


def save_results_llm(bank_name: str, language: str, db: Session, results: list):
    for res in results:
        exists = db.query(SentimentResultDB).filter(
            SentimentResultDB.url == res.url
        ).first()

        if not exists:
            db_result = SentimentResultDB(
                title=res.title,
                url=res.url,
                sentiment=res.sentiment,
                score=res.score,
                name=bank_name,
                language=language
            )
            db.add(db_result)

    db.commit()
