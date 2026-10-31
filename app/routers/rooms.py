from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field, StringConstraints, field_validator
from sqlmodel import col, select

from app.dependencies.database import SessionDep
from app.dependencies.room import getRoomId
from app.models.room import Room, RoomBase, RoomPublic, RoomUpdate

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)


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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[RoomPublic],
)
async def get_rooms(session: SessionDep, params: Annotated[RoomQueryParams, Query()]):

    statement = select(Room)

    if params.max_price:
        statement = statement.where(Room.price_per_night <= params.max_price)

    if params.search:
        statement = statement.where(col(Room.name).ilike(f"%{params.search}%"))

    rooms = await session.exec(statement)
    return rooms.all()

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


@router.get("/faq", status_code=status.HTTP_200_OK)
def get_room_faq():
    return {"check_in": "From 3pm", "check_out": "Untill 11Am"}


# getRoomId = Annotated[int, Path(ge=1, description="The id of the room to be")]

MAINTENANCE_MODE = False


def check_maintainenace_mode():
    if MAINTENANCE_MODE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is under maintenance. Try again later",
        )


@router.get(
    "/{room_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoomPublic,
)
async def getRoomById(
    session: SessionDep,
    room_id: getRoomId,
) -> Room:
    room = await session.get(Room, room_id)
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


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RoomPublic,
    dependencies=[Depends(check_maintainenace_mode)],
)
async def create_room(
    session: SessionDep,
    room: RoomBase,
):
    print("Payload", room)
    validated_room = Room.model_validate(room)
    print("Validated_Room", validated_room)
    session.add(validated_room)
    await session.commit()
    await session.refresh(validated_room)
    return validated_room


@router.patch(
    "/{room_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoomPublic,
    dependencies=[Depends(check_maintainenace_mode)],
)
async def update_room(
    session: SessionDep, room_id: getRoomId, room_payload: RoomUpdate
):

    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room Not Found"
        )
    room_payload_without_default_value = room_payload.model_dump(exclude_unset=True)
    room.sqlmodel_update(room_payload_without_default_value)
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


@router.delete(
    "/delete/{room_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_maintainenace_mode)],
)
async def delete_room(session: SessionDep, room_id: getRoomId) -> Room:
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room Not Found"
        )

    await session.delete(room)
    await session.commit()
    return room
