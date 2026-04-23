from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent  # → app/
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    api_key: str
    algorithm: str = 'HS256'
    

settings = Settings()


