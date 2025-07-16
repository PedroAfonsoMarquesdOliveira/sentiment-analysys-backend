from pydantic import BaseModel, Field
from typing import Optional, List

class BankRequest(BaseModel):
    bank_name: str
    language: str
    limit: int

class SentimentResult(BaseModel):
    title: Optional[str]
    url: Optional[str]
    sentiment: str
    score: float


class Source(BaseModel):
    id: Optional[str] = None
    name: str

class Article(BaseModel):
    source: Source
    author: Optional[str] = None
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    urlToImage: Optional[str] = Field(None, alias='image')
    publishedAt: Optional[str]
    content: Optional[str]
    model_config = {
        "validate_by_name": True
    }


class State(BaseModel):
    bank_name: str
    articles: Optional[List[Article]] = None
    results: Optional[List[SentimentResult]] = None
    error: Optional[str] = None
    language: str
    limit: int





