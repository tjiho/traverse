from contextlib import asynccontextmanager
from dataclasses import asdict

from fastapi import FastAPI

from utils.prepare import prepare
from utils.embedding_search import search
from utils.rerank_with_crossencoder import rerank
from utils.types import Candidate


@asynccontextmanager
async def lifespan(app: FastAPI):
    candidates, search_settings, rerank_settings = prepare()
    app.state.candidates = candidates
    app.state.search_settings = search_settings
    app.state.rerank_settings = rerank_settings
    yield


app = FastAPI(title="Traverse", lifespan=lifespan)


@app.get("/search")
def search_tags(query: str) -> list[Candidate]:
    results = search(query, app.state.candidates, app.state.search_settings)
    reranked = rerank(query, results, app.state.rerank_settings)
    return [asdict(c) for c in reranked]


@app.get("/health")
def health():
    return {"status": "ok"}
