from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "API-Pulse Backend"
    CORS_ORIGINS: list[str] = ["*"]
    MAX_CONCURRENCY_LIMIT: int = 10000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
