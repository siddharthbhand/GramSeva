from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL

# -------------------------------------------------------
# Add Backend Folder to Python Path
# -------------------------------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

# -------------------------------------------------------
# Import Project Settings
# -------------------------------------------------------

from app.core.config import settings
from app.db.database import Base

# Import all models here
from app.models.user import User
from app.models.department import Department

# -------------------------------------------------------
# Alembic Configuration
# -------------------------------------------------------

config = context.config

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

# Set URL for Alembic
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL.render_as_string(hide_password=False).replace("%", "%%")
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# -------------------------------------------------------
# Offline Migration
# -------------------------------------------------------

def run_migrations_offline():

    context.configure(
        url=DATABASE_URL.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------------
# Online Migration
# -------------------------------------------------------

def run_migrations_online():

    engine = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------------
# Run Migration
# -------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()