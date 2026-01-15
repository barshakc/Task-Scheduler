from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    
    class Config:
        env_file = ".env"  

settings = Settings()

