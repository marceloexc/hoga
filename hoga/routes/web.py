import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from hoga.shared.templates import templates
web = APIRouter()


@web.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

