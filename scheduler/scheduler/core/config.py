from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Ensure .env is loaded (useful for Celery and Streamlit)
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    
    class Config:
        env_file = ".env"

settings = Settings()

print("DATABASE_URL =", settings.DATABASE_URL)  
