from typing import Annotated

from fastapi import Path

getRoomId = Annotated[int, Path(ge=1, description="The id of the room to be")]
