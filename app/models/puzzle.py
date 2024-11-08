from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Puzzle(SQLModel, table=True, str_strip_whitespace=True):
    __tablename__ = "puzzle"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field()
    size: int = Field()
    created_at: datetime = Field(
        description="Creation timestamp",
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        description="Update timestamp",
        default_factory=datetime.now,
    )

    results: list["PuzzleResult"] = Relationship(back_populates="puzzle")
