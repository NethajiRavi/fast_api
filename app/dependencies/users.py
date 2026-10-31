from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from app.dependencies.database import SessionDep
from app.models.user import user

userId = Annotated[int, Path(ge=1, description="The id of user Need to fetch")]


async def get_user_404(
    session: SessionDep,
    user_id: userId,
) -> user:
    exist_user = await session.get(user, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return exist_user


UserDep = Annotated[user, Depends(get_user_404)]
