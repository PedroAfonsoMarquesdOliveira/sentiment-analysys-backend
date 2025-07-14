from pydantic import BaseModel
from typing import Optional, List

class BankRequest(BaseModel):
    bank_name: str
    language: str

class SentimentResult(BaseModel):
    title: Optional[str]
    url: Optional[str]
    sentiment: str
    score: float


class Source(BaseModel):
    id: Optional[str]
    name: str


class Article(BaseModel):
    source: Source
    author: Optional[str]
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    urlToImage: Optional[str]
    publishedAt: Optional[str]
    content: Optional[str]


class State(BaseModel):
    bank_name: str
    articles: Optional[List[Article]] = None
    results: Optional[List[SentimentResult]] = None
    error: Optional[str] = None
    language: str





