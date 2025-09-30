from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, select

from app.api import user_router, book_router
from app.api.users.models import User
from app.core.config import settings
from app.core.security import core_router
from app.api.users.utils import create_admin_user
from app.db.session import init_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with Session(engine) as session:
        existing = session.exec(
            select(User).where(User.is_superuser == True)
        ).first()
        if not existing:
            create_admin_user(session, "admin", "Admin", "admin")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(book_router, prefix="/books", tags=["Books"])
app.include_router(core_router, prefix="", tags=["Security"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
