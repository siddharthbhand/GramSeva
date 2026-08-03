from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.departments import router as department_router
from app.api.complaints import router as complaint_router
from app.api.complaint_assignments import (
    router as complaint_assignment_router,
)

from app.core.config import settings
from app.db.database import Base, engine

# Import all models
from app.models.user import User
from app.models.department import Department
from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Create database tables
Base.metadata.create_all(bind=engine)

# ============================
# Authentication
# ============================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

# ============================
# User Management
# ============================

app.include_router(users_router)

# ============================
# Department Management
# ============================

app.include_router(department_router)

# ============================
# Complaint Management
# ============================

app.include_router(complaint_router)

# ============================
# Complaint Assignment Management
# ============================

app.include_router(
    complaint_assignment_router
)

# ============================
# Default Routes
# ============================

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