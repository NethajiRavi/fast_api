from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from app.dependencies.database import SessionDep
from app.models.booking import Booking, BookingModel, BookingPublic
from app.models.room import Room
from app.models.user import user

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookingPublic)
async def create_booking(session: SessionDep, booking: BookingModel):
    room = await session.get(Room, booking.room_id)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room does not exist"
        )

    exist_user = await session.get(user, booking.user_id)
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist"
        )

    validated_booking = Booking.model_validate(booking)
    session.add(validated_booking)
    await session.commit()
    await session.refresh(validated_booking)
    return validated_booking


@router.get(
    "/{booking_id}", status_code=status.HTTP_200_OK, response_model=BookingPublic
)
async def get_booking(session: SessionDep, booking_id: Annotated[int, Path(ge=1)]):
    print(booking_id, "bookingId")
    booking = await session.get(Booking, booking_id)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking does not exist"
        )
    print(booking)
    return booking
