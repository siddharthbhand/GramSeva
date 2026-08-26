from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# =====================================================
# Database URL
# =====================================================

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)


# =====================================================
# Database Engine
# =====================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
)


# =====================================================
# Database Session
# =====================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =====================================================
# Base Model
# =====================================================

Base = declarative_base()


# =====================================================
# Database Dependency
# =====================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()