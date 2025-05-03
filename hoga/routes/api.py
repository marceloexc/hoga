import logging

from fastapi import APIRouter

api = APIRouter()


@api.get("/")
async def root_api():
    return "Hello from the api!"

