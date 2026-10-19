from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

import app.models.room as room

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# Request to hit route handler
# A route handler will have a dependencyon get session
# get_session will create a data bases sesssion
# get session will yield control to database session
# route handler will finish up
# the context manager (with) will clean up the session

SessionDep = Annotated[Session, Depends(get_session)]
