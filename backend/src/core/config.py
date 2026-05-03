import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")

settings = Settings()
