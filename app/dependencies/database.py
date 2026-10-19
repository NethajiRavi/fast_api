from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import app.models.room as room

sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

# database Need to configure asyn using lib
# eg for postgress --postgresql+asyncpg

engine = create_async_engine(sqlite_url, echo=True)


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    # SQLModel.metadata.create_all(engine)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session

    # with Session(engine) as session:
    #     yield session


# Request to hit route handler
# A route handler will have a dependencyon get session
# get_session will create a data bases sesssion
# get session will yield control to database session
# route handler will finish up
# the context manager (with) will clean up the session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
