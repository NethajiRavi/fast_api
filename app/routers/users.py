from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import selectinload

from app.dependencies.database import SessionDep
from app.dependencies.users import UserDep, userId
from app.models.booking import BookingPublic
from app.models.user import user, userBase, userPublic

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=userPublic)
async def create_user(session: SessionDep, users: userBase):
    validated_user = user.model_validate(users)
    session.add(validated_user)
    await session.commit()
    await session.refresh(validated_user)
    return validated_user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=userPublic)
async def get_user(user: UserDep):
    return user


@router.get(
    "/{user_id}/bookings",
    status_code=status.HTTP_200_OK,
    response_model=list[BookingPublic],
)
async def get_user_bookings(session: SessionDep, user_id: userId):
    exist_user = await session.get(
        user, user_id, options=[selectinload(user.bookings)]
    )  # type ignoring Eager Loading
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return exist_user.bookings
