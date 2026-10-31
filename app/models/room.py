from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.booking import Booking


# Base Model class- shared fields for all representation of a room
class RoomBase(SQLModel):
    name: str = Field()
    price_per_night: int = Field()
    bedrooms: float = Field(multiple_of=0.5)
    bathrooms: float = Field(multiple_of=0.5)


# Room table model - map to the room data base model
class Room(RoomBase, table=True):
    __tablename__: str = "rooms"
    id: int | None = Field(default=None, primary_key=True)
    bookings: list["Booking"] = Relationship(back_populates="room")


#  Room response modal
class RoomPublic(RoomBase):
    id: int


#  Room Update modal- all fields can be optinal beacuse
#  we are fall back to None
class RoomUpdate(SQLModel):
    name: str | None = None
    price_per_night: int | None = None
    bedrooms: float | None = None
    bathrooms: float | None = None
