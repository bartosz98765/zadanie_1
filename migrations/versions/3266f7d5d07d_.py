"""empty message

Revision ID: 3266f7d5d07d
Revises: 
Create Date: 2024-06-01 16:07:08.974171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3266f7d5d07d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tag",
        sa.Column("id", sa.VARCHAR(length=64), nullable=False),
        sa.Column("name", sa.VARCHAR(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tag")
