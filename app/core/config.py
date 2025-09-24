from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Store"
    VERSION: str = "0.0.1"

    DEBUG: bool = True
    SQLITE_URL: str | None = None
    POSTGRES_URL: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        return self.SQLITE_URL if self.DEBUG else self.POSTGRES_URL

    class Config:
        env_file = ".env"



settings = Settings()
