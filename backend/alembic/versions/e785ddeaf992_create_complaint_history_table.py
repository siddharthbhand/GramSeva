"""create complaint history table

Revision ID: e785ddeaf992
Revises: 63ecf856b0a8
Create Date: 2026-08-03 18:35:25.772882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e785ddeaf992"
down_revision: Union[str, Sequence[str], None] = "63ecf856b0a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    complaint_status_enum = sa.Enum(
        "Pending",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed",
        "Rejected",
        "Reopened",
        name="complaintstatus",
    )

    op.create_table(
        "complaint_history",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "complaint_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "old_status",
            complaint_status_enum,
            nullable=False,
        ),

        sa.Column(
            "new_status",
            complaint_status_enum,
            nullable=False,
        ),

        sa.Column(
            "changed_by",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "remarks",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),

        sa.ForeignKeyConstraint(
            ["changed_by"],
            ["users.id"],
        ),
    )

    op.create_index(
        "ix_complaint_history_id",
        "complaint_history",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_complaint_history_id",
        table_name="complaint_history",
    )

    op.drop_table("complaint_history")