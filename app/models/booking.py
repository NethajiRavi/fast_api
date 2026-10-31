from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.room import Room
    from app.models.user import user


# POST /booking -->{rooms_id, user_id}
class BookingModel(SQLModel):
    room_id: int
    user_id: int
    check_in: datetime
    check_out: datetime


class Booking(BookingModel, table=True):
    __tablename__: str = "bookings"
    id: int | None = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="rooms.id")
    user_id: int = Field(foreign_key="users.id")

    room: "Room" = Relationship(back_populates="bookings")
    user: "user" = Relationship(back_populates="bookings")


class BookingPublic(BookingModel):
    id: int
