"""add complaint status enum

Revision ID: 63ecf856b0a8
Revises: eda6ed1d9d4d
Create Date: 2026-08-03 10:45:49.637910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "63ecf856b0a8"
down_revision: Union[str, Sequence[str], None] = "eda6ed1d9d4d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Convert existing complaint status values
    op.execute("""
        UPDATE complaints
        SET status = 'PENDING'
        WHERE status = 'Pending'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'ASSIGNED'
        WHERE status = 'Assigned'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'IN_PROGRESS'
        WHERE status = 'In Progress'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'RESOLVED'
        WHERE status = 'Resolved'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'CLOSED'
        WHERE status = 'Closed'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'REJECTED'
        WHERE status = 'Rejected'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'REOPENED'
        WHERE status = 'Reopened'
    """)

    op.alter_column(
        "complaints",
        "status",
        existing_type=mysql.VARCHAR(length=50),
        type_=sa.Enum(
            "PENDING",
            "ASSIGNED",
            "IN_PROGRESS",
            "RESOLVED",
            "CLOSED",
            "REJECTED",
            "REOPENED",
            name="complaintstatus",
        ),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "complaints",
        "status",
        existing_type=sa.Enum(
            "PENDING",
            "ASSIGNED",
            "IN_PROGRESS",
            "RESOLVED",
            "CLOSED",
            "REJECTED",
            "REOPENED",
            name="complaintstatus",
        ),
        type_=mysql.VARCHAR(length=50),
        existing_nullable=False,
    )

    # Convert values back to previous format
    op.execute("""
        UPDATE complaints
        SET status = 'Pending'
        WHERE status = 'PENDING'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'Assigned'
        WHERE status = 'ASSIGNED'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'In Progress'
        WHERE status = 'IN_PROGRESS'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'Resolved'
        WHERE status = 'RESOLVED'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'Closed'
        WHERE status = 'CLOSED'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'Rejected'
        WHERE status = 'REJECTED'
    """)

    op.execute("""
        UPDATE complaints
        SET status = 'Reopened'
        WHERE status = 'REOPENED'
    """)