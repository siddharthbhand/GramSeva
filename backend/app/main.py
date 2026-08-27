import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.departments import router as department_router
from app.api.complaints import router as complaint_router
from app.api.admin_analytics import (
    router as admin_analytics_router,
)
from app.api.complaint_assignments import (
    router as complaint_assignment_router,
)
from app.api.complaint_history import (
    router as complaint_history_router,
)
from app.api.complaint_escalation import (
    router as complaint_escalation_router,
)
from app.api.notification import (
    router as notification_router,
)

from app.core.config import settings
from app.db.database import SessionLocal
from app.services.sla_automation_service import (
    SLAAutomationService,
)


# =====================================================
# SLA Monitoring Configuration
# =====================================================

SLA_MONITOR_INTERVAL_SECONDS = 300


# =====================================================
# SLA Background Monitor
# =====================================================

async def sla_monitor_loop():
    """
    Periodically process SLA near-breach warnings
    and automatic SLA breach escalations.
    """

    while True:

        db = SessionLocal()

        try:
            SLAAutomationService.process_near_breach_complaints(
                db=db,
            )

            SLAAutomationService.process_breached_complaints(
                db=db,
            )

        except Exception:
            db.rollback()

        finally:
            db.close()

        await asyncio.sleep(
            SLA_MONITOR_INTERVAL_SECONDS
        )


# =====================================================
# Application Lifespan
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    monitor_task = asyncio.create_task(
        sla_monitor_loop()
    )

    try:
        yield

    finally:
        monitor_task.cancel()

        try:
            await monitor_task
        except asyncio.CancelledError:
            pass


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)


# =====================================================
# CORS Configuration
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Global Database Error Handler
# =====================================================

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "A database error occurred. "
                "Please try again later."
            )
        },
    )


# =====================================================
# Global Unexpected Error Handler
# =====================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "An unexpected server error occurred. "
                "Please try again later."
            )
        },
    )


# =====================================================
# Authentication
# =====================================================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)


# =====================================================
# User Management
# =====================================================

app.include_router(
    users_router,
)


# =====================================================
# Department Management
# =====================================================

app.include_router(
    department_router,
)


# =====================================================
# Complaint Management
# =====================================================

app.include_router(
    complaint_router,
)


# =====================================================
# Complaint Assignment Management
# =====================================================

app.include_router(
    complaint_assignment_router,
)


# =====================================================
# Complaint History Management
# =====================================================

app.include_router(
    complaint_history_router,
)


# =====================================================
# Complaint Escalation Management
# =====================================================

app.include_router(
    complaint_escalation_router,
)


# =====================================================
# Notification Management
# =====================================================

app.include_router(
    notification_router,
)


# =====================================================
# Admin Analytics
# =====================================================

app.include_router(
    admin_analytics_router,
)


# =====================================================
# Default Routes
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to GramSeva API"
    }


# =====================================================
# Environment Check
# =====================================================

@app.get("/check-env")
def check_env():
    return {
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database": settings.DB_NAME,
        "user": settings.DB_USER,
    }


# =====================================================
# Database Health Check
# =====================================================

@app.get("/test-db")
def test_db():
    return {
        "message": "Database Connected Successfully"
    }