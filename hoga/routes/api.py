from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from hoga.database import get_db
from hoga.models import Directory, Post
from hoga.schemas import DirectorySchema, GalleryResponse

api_v1 = APIRouter()


@api_v1.get("/status")
def index():
    return "Running! (Go catch it!!!)"


@api_v1.get("/list", response_model=List[DirectorySchema])
def list_galleries(db: Session = Depends(get_db)):
    directories = db.query(Directory).all()
    return directories


@api_v1.get("/galleries", response_model=GalleryResponse)
def post_listing(
        hoga_id: int,
        db: Session = Depends(get_db)
):
    all_posts = db.query(Post).filter_by(directory_id=hoga_id).all()
    return {"gallery": all_posts}
