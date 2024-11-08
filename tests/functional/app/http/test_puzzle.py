from tests.fixtures import database_fixture, client_fixture, faker_fixture

from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from main import app
from app.models.puzzle import Puzzle
from app.models.puzzle_result import PuzzleResult


def test_store(monkeypatch, client: TestClient):
    def mock_execute_n_queen_puzzle_job():
        assert True

    monkeypatch.setattr(
        "app.jobs.n_queens_job.execute_n_queen_puzzle_job",
        mock_execute_n_queen_puzzle_job,
    )

    payload = Puzzle(size=4, name="My puzzle name")

    response = client.post(
        app.url_path_for("api.v1.puzzle.store"),
        json=payload.model_dump(include=["size", "name"]),
    )

    data: dict = response.json()

    assert response.status_code == 201
    assert data.get("name") == payload.name
    assert data.get("size") == payload.size


def test_store_empty_payload(client: TestClient):
    response = client.post(
        app.url_path_for("api.v1.puzzle.store"),
        json={},
    )

    assert response.status_code == 422


def test_store_invalid_payload(client: TestClient):
    response = client.post(
        app.url_path_for("api.v1.puzzle.store"),
        json={"size": -2, "name": "       "},
    )

    assert response.status_code == 422


def test_fetch_one(session: Session, client: TestClient, faker: Faker):
    puzzle = Puzzle(name=faker.name(), size=faker.random_digit_not_null())

    session.add(puzzle)
    session.commit()
    session.refresh(puzzle)

    response = client.get(
        app.url_path_for("api.v1.puzzle.fetch_one", puzzle_id=puzzle.id),
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == puzzle.id
    assert data["name"] == puzzle.name
    assert data["size"] == puzzle.size


def test_fet_one_not_found(client: TestClient):
    response = client.get(
        app.url_path_for("api.v1.puzzle.fetch_one", puzzle_id="999999999"),
    )

    assert response.status_code == 404


def test_fetch_success(session: Session, client: TestClient, faker: Faker):
    puzzle = Puzzle(name=faker.name(), size=faker.random_digit_not_null())
    puzzle_trap = Puzzle(name=faker.name(), size=faker.random_digit_not_null())
    result_1 = PuzzleResult(
        puzzle=puzzle, algorithm="algorithm", board=[[1, 2], [1, 3]]
    )
    result_2 = PuzzleResult(
        puzzle=puzzle, algorithm="algorithm", board=[[2, 2], [2, 3]]
    )
    result_3 = PuzzleResult(
        puzzle=puzzle, algorithm="algorithm", board=[[2, 6], [7, 3]]
    )
    result_4 = PuzzleResult(
        puzzle=puzzle_trap, algorithm="algorithm", board=[[2, 6], [7, 3]]
    )

    session.add(result_1)
    session.add(result_2)
    session.add(result_3)
    session.add(result_4)
    session.commit()

    response = client.get(
        app.url_path_for("api.v1.puzzle.rel.result.fetch", puzzle_id=puzzle.id),
    )

    result = response.json()

    assert response.status_code == 200
    assert len(result) == 3


def test_fetch_empty_success(session: Session, client: TestClient, faker: Faker):
    puzzle = Puzzle(name=faker.name(), size=faker.random_digit_not_null())

    session.add(puzzle)
    session.commit()

    response = client.get(
        app.url_path_for("api.v1.puzzle.rel.result.fetch", puzzle_id=puzzle.id),
    )

    result = response.json()

    assert response.status_code == 200
    assert len(result) == 0


def test_fetch_not_found(client: TestClient):
    response = client.get(
        app.url_path_for("api.v1.puzzle.rel.result.fetch", puzzle_id=99999999999999999),
    )

    assert response.status_code == 404
