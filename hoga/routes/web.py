import logging

from fastapi import APIRouter
from starlette.responses import HTMLResponse

web = APIRouter()


@web.get("/")
async def root():
    return HTMLResponse("<h1>Hello internet!</h1>")

