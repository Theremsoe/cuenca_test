from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

from config.database import DatabaseConfig

"""
Database engine configuration and definition.
TOD: we must move up to provider file
"""
db_config = DatabaseConfig.make()

engine = create_engine(str(db_config.uri), connect_args={})


def migrate_db() -> None:
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
