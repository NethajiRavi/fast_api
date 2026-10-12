# from typing import Annotated

# from fastapi import FastAPI, HTTPException, Query, status
# from fastapi.staticfiles import StaticFiles
# from pydantic import AfterValidator

# app = FastAPI()

# app.mount("/assets", StaticFiles(directory="assets"), name="assets")


# # Annotated Comes from 'typing'
# # Annotated Type attached from a existing type

# # str
# # value: Annotaed[str,"hello"]

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


# def fail_if_funny(search: str):
#     if "lol" in search:
#         raise ValueError("No Funny Business is Allowded")
#     return search


# search_query_validator = Query(
#     min_length=3,
#     max_length=6,
#     title="Search term",
#     description="Proide a keyword to look for with in the room title",
# )


# search_humor_ban_validator = AfterValidator(fail_if_funny)


# @app.get("/", status_code=status.HTTP_200_OK)
# def root():
#     return {"Message": "Welcome To Rent Rooms"}


# @app.get("/rooms", status_code=status.HTTP_200_OK)
# def get_rooms(
#     price: Annotated[int | None, Query(ge=150, le=1000)] = None,
#     search: Annotated[
#         str | None,
#         search_query_validator,
#         search_humor_ban_validator,
#     ] = None,
# ):
#     result = [house, studio, apartment]
#     if price:
#         return [room for room in result if room["price_per_night"] <= price]
#     if search:
#         return [room for room in result if search.lower() in room["name"].lower()]
#     return result

#     # collection = []
#     # for rooms in [apartment, studio, house]:
#     #     if search.lower() in rooms["name"].lower():
#     #         if price is None or rooms["price_per_night"] <= price:
#     #             collection.append(rooms)
#     # return collection

#     # return [rooms for rooms in collection if search.lower() in rooms["name"].lower()]


# @app.get("/rooms/faq", status_code=status.HTTP_200_OK)
# def get_room_faq():
#     return {"check_in": "From 3pm", "check_out": "Untill 11Am"}


# @app.get("/rooms/{room_id}", status_code=status.HTTP_200_OK)
# def getRoomById(room_id: int):
#     for room in [apartment, house, studio]:
#         if room["id"] == room_id:
#             return room

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room Not Found")
