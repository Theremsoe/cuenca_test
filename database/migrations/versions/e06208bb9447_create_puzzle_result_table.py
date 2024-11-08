"""Create Puzzle Result table

Revision ID: e06208bb9447
Revises: 21e3391eaf8c
Create Date: 2024-11-07 15:48:12.304293

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e06208bb9447"
down_revision: Union[str, None] = "21e3391eaf8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "puzzle_result",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("puzzle_id", sa.BigInteger),
        sa.Column("algorithm", sa.String),
        sa.Column("board", sa.JSON),
        sa.Column("duration", sa.BigInteger, default=0),
        sa.Column("created_at", sa.TIMESTAMP),
        sa.Column("updated_at", sa.TIMESTAMP),
    )


def downgrade() -> None:
    op.drop_table("puzzle_result")
