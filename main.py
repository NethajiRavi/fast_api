from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, StringConstraints, field_validator
from sqlmodel import col, func, select

from database import SessionDep, create_db_tables
from models import Room, RoomBase, RoomPublic, RoomUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    #  Additional operation before the sever startup
    create_db_tables()
    yield
    #  Additional operation after the sever startup


app = FastAPI(lifespan=lifespan)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")


# Annotated Comes from 'typing'
# Annotated Type attached from a existing type

# str
# value: Annotaed[str,"hello"]

apartment = {
    "id": 1,
    "name": "sunny 2 bedroom apartment",
    "price_per_night": 200,
    "bedrooms": 2,
    "bathrooms": 2,
}

house = {
    "id": 2,
    "name": "coszy 3 bedroom apartment",
    "price_per_night": 350,
    "bedrooms": 3,
    "bathrooms": 2,
}
studio = {
    "id": 3,
    "name": "Mordern studion near Museum",
    "price_per_night": 150,
    "bedrooms": 1,
    "bathrooms": 1,
}


class AppCookie(BaseModel):
    theme: Literal["dark", "light"] = Field(default="dark")
    languange: Literal["en", "es", "fr"] = "en"


class RoomQueryParams(BaseModel):
    max_price: int | None = Field(default=None, ge=150, le=1000)

    search: Annotated[
        str | None,
        StringConstraints(to_lower=True),
        Field(
            default=None,
            min_length=3,
            max_length=6,
            title="Search term",
            description="Proide a keyword to look for with in the room title",
        ),
    ]

    @field_validator("search")
    @classmethod
    def fail_if_funny(cls, search: str) -> str:
        if "lol" in search:
            raise ValueError("No Funny Business is Allowded")
        return search


@app.get("/", status_code=status.HTTP_200_OK)
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


@app.get("/rooms", status_code=status.HTTP_200_OK, response_model=list[RoomPublic])
def get_rooms(session: SessionDep, params: Annotated[RoomQueryParams, Query()]):

    statement = select(Room)

    if params.max_price:
        statement = statement.where(Room.price_per_night <= params.max_price)

    if params.search:
        statement = statement.where(col(Room.name).ilike(f"%{params.search}%"))

    return session.exec(statement).all()

    # select(Room).where(Room.name == "sunny 2_bedroom appartment")
    # result = session.exec(select(Room)).all()
    # print(result)
    # # result = [house, studio, apartment]
    # if params.max_price:
    #     result = [room for room in result if room.price_per_night <= result.max_price]
    # if params.search:
    #     result = [room for room in result if params.search in room.name.lower()]
    # return result

    # collection = []
    # for rooms in [apartment, studio, house]:
    #     if search.lower() in rooms["name"].lower():
    #         if price is None or rooms["price_per_night"] <= price:
    #             collection.append(rooms)
    # return collection

    # return [rooms for rooms in collection if search.lower() in rooms["name"].lower()]


@app.get("/rooms/faq", status_code=status.HTTP_200_OK)
def get_room_faq():
    return {"check_in": "From 3pm", "check_out": "Untill 11Am"}


getRoomId = Annotated[int, Path(ge=1, description="The id of the room to be")]


@app.get("/rooms/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomPublic)
def getRoomById(
    session: SessionDep,
    room_id: getRoomId,
) -> Room:
    room = session.get(Room, room_id)
    # with Session(engine) as session:
    #     # python code to interact db

    # for room in [apartment, house, studio]:
    #     if room["id"] == room_id:
    #         return room

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room Not Found"
        )

    return room


@app.get("/preference", status_code=status.HTTP_200_OK)
def set_preference(response: Response):
    appCookied = AppCookie()
    response.set_cookie(key="theme", value=appCookied.theme)
    response.set_cookie(key="language", value=appCookied.languange)
    return {"message": "Preference are updated"}


@app.post("/rooms", status_code=status.HTTP_201_CREATED, response_model=RoomPublic)
def create_room(session: SessionDep, room: RoomBase):
    print("Payload", room)
    validated_room = Room.model_validate(room)
    print("Validated_Room", validated_room)
    session.add(validated_room)
    session.commit()
    session.refresh(validated_room)
    return validated_room


@app.patch(
    "/rooms/{room_id}", status_code=status.HTTP_200_OK, response_model=RoomPublic
)
def update_room(session: SessionDep, room_id: getRoomId, room_payload: RoomUpdate):

    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room Not Found"
        )
    room_payload_without_default_value = room_payload.model_dump(exclude_unset=True)
    room.sqlmodel_update(room_payload_without_default_value)
    session.add(room)
    session.commit()
    session.refresh(room)
    return room


@app.delete("/delete/{room_id}", status_code=status.HTTP_200_OK)
def delete_room(session: SessionDep, room_id: getRoomId) -> Room:
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room Not Found"
        )

    session.delete(room)
    session.commit()
    return room
