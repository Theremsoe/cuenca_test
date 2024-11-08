from typing import Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
from sqlmodel import select

from sqlalchemy import desc

from app.request.puzzle import PuzzleRequest
from app.models.puzzle import Puzzle
from app.models.puzzle_result import PuzzleResult
from app.jobs.n_queens_job import execute_n_queen_puzzle_job
from providers.database import SessionDep

http_puzzle_router = APIRouter(prefix="/puzzle")


@http_puzzle_router.post(
    "/", status_code=201, name="api.v1.puzzle.store", operation_id="puzzle.store"
)
def store(
    payload: PuzzleRequest, session: SessionDep, background_task: BackgroundTasks
) -> Puzzle:
    puzzle = Puzzle(size=payload.size, name=payload.name)

    session.add(puzzle)
    session.commit()
    session.refresh(puzzle)

    background_task.add_task(execute_n_queen_puzzle_job, session, puzzle)

    return puzzle


@http_puzzle_router.get(
    "/{puzzle_id}",
    name="api.v1.puzzle.fetch_one",
    operation_id="puzzle.fetch_one",
)
def fetch_one(puzzle_id: int, session: SessionDep) -> Puzzle:
    puzzle: Optional[Puzzle] = session.get(Puzzle, puzzle_id)

    if not puzzle:
        raise HTTPException(status_code=404, detail="Resource not found")

    return puzzle


@http_puzzle_router.get(
    "/{puzzle_id}/results",
    name="api.v1.puzzle.rel.result.fetch",
    operation_id="puzzle.rel.result.fetch",
)
def fetch(
    puzzle_id: int,
    session: SessionDep,
    timestamp: datetime | None = None,
) -> list[PuzzleResult]:
    puzzle: Optional[Puzzle] = session.get(Puzzle, puzzle_id)

    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    ts: datetime = timestamp if timestamp else datetime.now()

    query = (
        select(PuzzleResult)
        .where(
            PuzzleResult.puzzle_id == puzzle.id,
            PuzzleResult.created_at <= ts.isoformat(),
        )
        .order_by(desc(PuzzleResult.created_at))
        .limit(50)
    )

    result = session.scalars(query)

    return result.all()
