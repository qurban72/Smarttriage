import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
# Railway gives "postgresql://" or "postgres://"; SQLAlchemy needs the psycopg driver
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "smarttriage-faqs")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

CATEGORY_MODEL = os.getenv("CATEGORY_MODEL", "your-hf-user/smarttriage-category")
URGENCY_MODEL = os.getenv("URGENCY_MODEL", "your-hf-user/smarttriage-urgency")

CONF_CLASSIFIER = float(os.getenv("CONF_CLASSIFIER", "0.75"))
CONF_RETRIEVAL = float(os.getenv("CONF_RETRIEVAL", "0.80"))

CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]
