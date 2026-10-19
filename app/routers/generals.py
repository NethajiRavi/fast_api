from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import APIRouter, Cookie, Header, Response, status
from pydantic import BaseModel, Field
from sqlmodel import select

from app.dependencies.database import SessionDep, create_db_tables

router = APIRouter()


class AppCookie(BaseModel):
    theme: Literal["dark", "light"] = Field(default="dark")
    languange: Literal["en", "es", "fr"] = "en"


@router.get("/", status_code=status.HTTP_200_OK)
def root(
    app_cookies: Annotated[AppCookie, Cookie()],
    user_agent: Annotated[str | None, Header()],
    session: SessionDep,
):

    db_result = session.exec(select(5)).one()

    greeting = {
        "en": "Welcome To Rendal Roome",
        "es": "asd asdfsdf",
        "fr": "sdfghj dfg",
    }

    greet = greeting.get(app_cookies.languange)

    return {"Message": greet, "UserAgent": user_agent, "db_result": db_result}


@router.get("/preference", status_code=status.HTTP_200_OK)
def set_preference(response: Response):
    appCookied = AppCookie()
    response.set_cookie(key="theme", value=appCookied.theme)
    response.set_cookie(key="language", value=appCookied.languange)
    return {"message": "Preference are updated"}
