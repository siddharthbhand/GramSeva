from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.config import settings
from app.db.database import Base, engine

# Import all models
from app.models.user import User

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Authentication Routes
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# User Management Routes
app.include_router(users_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to GramSeva API"
    }


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
        "message": "Database Connected Successfully"
    }