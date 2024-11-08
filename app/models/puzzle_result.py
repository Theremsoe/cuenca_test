from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, Column, BigInteger
from sqlalchemy.ext.mutable import MutableList
from datetime import datetime
from uuid import UUID
from app.models.puzzle import Puzzle
from uuid_v9 import uuidv9


class PuzzleResult(SQLModel, table=True, str_strip_whitespace=True):
    __tablename__ = "puzzle_result"

    id: UUID = Field(primary_key=True, default_factory=lambda: UUID(uuidv9()))

    puzzle_id: int = Field(foreign_key="puzzle.id")
    puzzle: Puzzle = Relationship(back_populates="results")

    algorithm: str = Field()
    board: list[list[int]] = Field(
        sa_column=Column(MutableList.as_mutable(JSON(none_as_null=True))),
        default=[],
    )
    duration: int = Field(sa_column=Column(BigInteger), default=0)

    created_at: datetime = Field(
        description="Creation timestamp",
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        description="Update timestamp",
        default_factory=datetime.now,
    )
