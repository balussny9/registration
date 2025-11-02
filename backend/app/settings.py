from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./data/ssp.db"
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"
    UPLOAD_DIR: str = "./uploads"  # relative to backend working dir

    class Config:
        env_file = ".env"

settings = Settings()
