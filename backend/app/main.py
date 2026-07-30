from fastapi import FastAPI

from app.core.config import settings
from app.db.database import Base, engine

# Import all models here
from app.models.user import User

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Create all database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Welcome to GramSeva API 🚀"
    }

from app.core.config import settings

@app.get("/check-env")
def check_env():
    return {
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database": settings.DB_NAME,
        "user": settings.DB_USER,
        "password": settings.DB_PASSWORD,
    }


@app.get("/test-db")
def test_db():
    return {
        "message": "Database Connected Successfully ✅"
    }

