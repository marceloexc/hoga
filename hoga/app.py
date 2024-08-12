import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from hoga.database import engine
from hoga.models import Base
from hoga.routes.media import media
from hoga.routes.api import api_v1
from hoga.routes.routes import router
from hoga.utils.compile_scss import compile_scss


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup routines
    compile_scss()
    yield


app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Logger initalized.")

# Include routers
app.include_router(router)
app.include_router(api_v1, prefix="/api")
app.include_router(media, prefix="/media")

# Create database columns
Base.metadata.create_all(bind=engine)

# Mount static files
app.mount("/static", StaticFiles(directory="hoga/static"), name="static")

