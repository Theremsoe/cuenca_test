from tests.fixtures import database_fixture, client_fixture, faker_fixture

from unittest import mock
from sqlmodel import Session
from sqlalchemy import func

from app.models.puzzle import Puzzle
from app.models.puzzle_result import PuzzleResult
from app.jobs.n_queens_job import execute_n_queen_puzzle_job


@mock.patch("app.jobs.n_queens_job.NQueensBacktracking")
def test_skips_empy_results(mock_NQueens, session: Session):
    execute_n_queen_puzzle_job(session, Puzzle(name="", size=2))
    execute_n_queen_puzzle_job(session, Puzzle(name="", size=0))
    execute_n_queen_puzzle_job(session, Puzzle(name="", size=3))

    assert mock_NQueens.return_value.call_count == 0


@mock.patch("app.jobs.n_queens_job.NQueensBacktracking")
def test_puzzle_dfs_strategy_is_executed(mock_NQueens, session: Session):
    puzzle = Puzzle(name="", size=8)

    session.add(puzzle)
    session.commit()

    mock_NQueens.return_value.solveNQueens.return_value = []

    execute_n_queen_puzzle_job(session, puzzle)

    assert mock_NQueens.call_count == 1


def test_results_are_stored(session: Session):
    puzzle = Puzzle(name="", size=4)

    session.add(puzzle)
    session.commit()

    execute_n_queen_puzzle_job(session, puzzle)

    session.refresh(puzzle)

    assert len(puzzle.results) == 1
