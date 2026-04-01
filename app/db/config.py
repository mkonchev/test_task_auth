from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5438"
    DB_NAME: str = "db_auth"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1111"
    JWT_SECRET: str = "secret-key"
    JWT_ALGORITHM: str = "HS256"
    EXP_AT: int = 900


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"localhost:{settings.DB_PORT}/{settings.DB_NAME}")
