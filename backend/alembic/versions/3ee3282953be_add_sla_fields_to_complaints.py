"""add_sla_fields_to_complaints

Revision ID: 3ee3282953be
Revises: e785ddeaf992
Create Date: 2026-08-03 20:13:22.994275

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ee3282953be"
down_revision: Union[str, Sequence[str], None] = "e785ddeaf992"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "complaints",
        sa.Column(
            "sla_hours",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("24"),
        ),
    )

    op.add_column(
        "complaints",
        sa.Column(
            "sla_due_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "complaints",
        sa.Column(
            "is_sla_breached",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("complaints", "is_sla_breached")
    op.drop_column("complaints", "sla_due_at")
    op.drop_column("complaints", "sla_hours")