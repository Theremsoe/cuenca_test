from datetime import datetime

from app.models.puzzle import Puzzle
from app.models.puzzle_result import PuzzleResult
from providers.database import SessionDep
from providers.puzzles.backtracking import NQueensBacktracking


def format_space_time(algorithm: str, runtime_diff: int):
    for prefix in [("ms", 1000), ("seconds", 1000), ("minutes", 60), ("hours", 60)]:
        if runtime_diff > prefix[1]:
            runtime_diff /= prefix[1]

        else:
            print(
                f"N Queen puzzle resolved with: {algorithm}. \n\rRuntime execution: {runtime_diff} {prefix[0]}"
            )
            break


def execute_n_queen_puzzle_job(
    session: SessionDep, puzzle: Puzzle, algorithm: str = "backtracking"
):
    print(f">>> {execute_n_queen_puzzle_job.__name__} job executed.")

    if puzzle.size < 1 or puzzle.size == 2 or puzzle.size == 3:
        return

    runtime_diff = 0

    if algorithm == "backtracking":
        start_time = datetime.now()
        n_queens = NQueensBacktracking()
        board = n_queens.solveNQueens(puzzle.size)
        end_time = datetime.now()

        runtime_diff = int((end_time - start_time).total_seconds() * 1000)

        result = PuzzleResult(
            algorithm="backtracking", board=board, duration=runtime_diff, puzzle=puzzle
        )

        session.add(result)
        session.commit()

    format_space_time(algorithm, runtime_diff)
