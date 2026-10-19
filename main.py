from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.dependencies.database import create_db_tables
from app.routers import generals, rooms


def log_request(request: Request):
    print(f"{request.method}/{request.url}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    #  Additional operation before the sever startup
    await create_db_tables()
    yield
    #  Additional operation after the sever startup


app = FastAPI(lifespan=lifespan, dependencies=[Depends(log_request)])
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.include_router(generals.router)
app.include_router(rooms.router)

# Annotated Comes from 'typing'
# Annotated Type attached from a existing type

# str
# value: Annotaed[str,"hello"]

# apartment = {
#     "id": 1,
#     "name": "sunny 2 bedroom apartment",
#     "price_per_night": 200,
#     "bedrooms": 2,
#     "bathrooms": 2,
# }

# house = {
#     "id": 2,
#     "name": "coszy 3 bedroom apartment",
#     "price_per_night": 350,
#     "bedrooms": 3,
#     "bathrooms": 2,
# }
# studio = {
#     "id": 3,
#     "name": "Mordern studion near Museum",
#     "price_per_night": 150,
#     "bedrooms": 1,
#     "bathrooms": 1,
# }
