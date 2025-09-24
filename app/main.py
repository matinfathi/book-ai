from fastapi import FastAPI

from app.api.v1 import books
from app.core import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_route(books.router, prefix="/books", tags=["Books"])


@app.get("/health")
def health():
    return {"status": "ok"}
