from sqlmodel import Field, SQLModel


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
