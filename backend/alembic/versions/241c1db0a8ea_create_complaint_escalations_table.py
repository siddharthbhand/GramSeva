"""create complaint escalations table

Revision ID: 241c1db0a8ea
Revises: 3ee3282953be
Create Date: 2026-08-06 08:34:13.587202

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "241c1db0a8ea"
down_revision: Union[str, Sequence[str], None] = "3ee3282953be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "complaint_escalations",

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
            "escalation_level",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),

        sa.Column(
            "escalated_to",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "escalated_by",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "reason",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "remarks",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("1"),
        ),

        sa.Column(
            "escalated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),

        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),

        sa.ForeignKeyConstraint(
            ["escalated_to"],
            ["users.id"],
        ),

        sa.ForeignKeyConstraint(
            ["escalated_by"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_complaint_escalations_id"),
        "complaint_escalations",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_complaint_escalations_id"),
        table_name="complaint_escalations",
    )

    op.drop_table("complaint_escalations")