from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import books
from app.core import settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(books.router, prefix="/books", tags=["Books"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
