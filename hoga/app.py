import logging
from contextlib import asynccontextmanager

import jinjax
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from hoga.routes.api import api
from hoga.routes.web import web


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup routines
    # compile_scss()
    yield

app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Logger initalized.")

app.include_router(api, prefix="/api")
app.include_router(web)

