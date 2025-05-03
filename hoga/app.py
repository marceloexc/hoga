import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from hoga.utils.compile_scss import compile_scss


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup routines
    # compile_scss()
    yield


app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Logger initalized.")

