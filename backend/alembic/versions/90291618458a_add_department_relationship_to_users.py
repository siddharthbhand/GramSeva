"""add department relationship to users

Revision ID: 90291618458a
Revises: feb45ead38b1
Create Date: 2026-08-15 22:19:19.094229

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "90291618458a"
down_revision: Union[str, Sequence[str], None] = "feb45ead38b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add department relationship to users."""

    # Add nullable department_id so existing users remain valid.
    op.add_column(
        "users",
        sa.Column(
            "department_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # Index for department-based user queries.
    op.create_index(
        op.f("ix_users_department_id"),
        "users",
        ["department_id"],
        unique=False,
    )

    # Connect users to departments.
    op.create_foreign_key(
        "fk_users_department_id_departments",
        "users",
        "departments",
        ["department_id"],
        ["id"],
    )


def downgrade() -> None:
    """Remove department relationship from users."""

    op.drop_constraint(
        "fk_users_department_id_departments",
        "users",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_users_department_id"),
        table_name="users",
    )

    op.drop_column(
        "users",
        "department_id",
    )