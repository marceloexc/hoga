import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.database import engine
from src.models import Base
from src.routes.api import api_v1
from src.routes.routes import router


# Initialize FastAPI app
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Logger initalized.")

# Include routers
app.include_router(router)
app.include_router(api_v1)

# Create database columns
Base.metadata.create_all(bind=engine)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

