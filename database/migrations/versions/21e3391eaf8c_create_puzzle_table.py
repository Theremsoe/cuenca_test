"""Create Puzzle table

Revision ID: 21e3391eaf8c
Revises:
Create Date: 2024-11-07 15:32:47.759803

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "21e3391eaf8c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "puzzle",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("name", sa.VARCHAR),
        sa.Column(
            "size",
            sa.SmallInteger,
        ),
        sa.Column("created_at", sa.TIMESTAMP),
        sa.Column("updated_at", sa.TIMESTAMP),
    )


def downgrade() -> None:
    op.drop_table("puzzle")
