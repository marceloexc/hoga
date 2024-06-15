from fastapi import APIRouter, Depends

api_v1 = APIRouter()


@api_v1.get("/api/")
def api_index():
    print("i am in the api index!")
    return {"hello":32}