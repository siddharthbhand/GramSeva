"""create notifications table

Revision ID: feb45ead38b1
Revises: 241c1db0a8ea
Create Date: 2026-08-11 23:32:58.716398

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# =====================================================
# Revision identifiers
# =====================================================

revision: str = "feb45ead38b1"

down_revision: Union[str, Sequence[str], None] = "241c1db0a8ea"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


# =====================================================
# Upgrade
# =====================================================

def upgrade() -> None:
    """Create notifications table."""

    op.create_table(
        "notifications",

        # -------------------------------------------------
        # Primary Key
        # -------------------------------------------------

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        # -------------------------------------------------
        # Notification Recipient
        # -------------------------------------------------

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        # -------------------------------------------------
        # Related Complaint
        # -------------------------------------------------

        sa.Column(
            "complaint_id",
            sa.Integer(),
            nullable=True,
        ),

        # -------------------------------------------------
        # Related Escalation
        # -------------------------------------------------

        sa.Column(
            "escalation_id",
            sa.Integer(),
            nullable=True,
        ),

        # -------------------------------------------------
        # Notification Content
        # -------------------------------------------------

        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "message",
            sa.Text(),
            nullable=False,
        ),

        # -------------------------------------------------
        # Notification Type
        # -------------------------------------------------

        sa.Column(
            "notification_type",
            sa.String(length=50),
            nullable=False,
        ),

        # -------------------------------------------------
        # Read Status
        # -------------------------------------------------

        sa.Column(
            "is_read",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("0"),
        ),

        sa.Column(
            "read_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        # -------------------------------------------------
        # Active Status
        # -------------------------------------------------

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("1"),
        ),

        # -------------------------------------------------
        # Timestamp
        # -------------------------------------------------

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        # -------------------------------------------------
        # Foreign Keys
        # -------------------------------------------------

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),

        sa.ForeignKeyConstraint(
            ["escalation_id"],
            ["complaint_escalations.id"],
        ),

        # -------------------------------------------------
        # Primary Key
        # -------------------------------------------------

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    # =====================================================
    # Notification ID Index
    # =====================================================

    op.create_index(
        op.f("ix_notifications_id"),
        "notifications",
        ["id"],
        unique=False,
    )


# =====================================================
# Downgrade
# =====================================================

def downgrade() -> None:
    """Drop notifications table."""

    op.drop_index(
        op.f("ix_notifications_id"),
        table_name="notifications",
    )

    op.drop_table(
        "notifications",
    )