import logging

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from hoga.database import get_db

media = APIRouter()


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@media.get("/{gallery}/{filename}", response_class=FileResponse)
def get_media(gallery: int, filename: str, db: Session = Depends(get_db)):
    raise NotImplementedError
