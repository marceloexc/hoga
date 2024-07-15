from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Directory, Post
from src.schemas import DirectorySchema, BPost
from typing import List

api_v1 = APIRouter()


@api_v1.get("/")
def index():
    return {"message": "Hello, World!"}


@api_v1.get("/list", response_model=List[DirectorySchema])
def list_galleries(db: Session = Depends(get_db)):
    directories = db.query(Directory).all()
    return directories


@api_v1.get("/gallery", response_model=List[BPost])
def post_listing(
        hoga_id: int,
        db: Session = Depends(get_db)
):
    all_posts = db.query(Post).filter_by(directory_id=hoga_id).all()
    return all_posts
