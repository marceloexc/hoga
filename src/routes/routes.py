import logging
import os
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Directory, Post
from src.plugins.twitter_media_downloader import furyutei_twitter_media_downloader
from src.utils import fetcher
from src.shared import templates

router = APIRouter()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)



@router.get("/", response_class=HTMLResponse)
def get_index(req: Request, db: Session = Depends(get_db)):
    directories = db.query(Directory).all()
    return templates.TemplateResponse(
        "index.html",
        context={"request": req, "directories": directories}
    )


@router.post("/update", response_class=HTMLResponse)
def post_query(image_folder: str = Form(...)):
    downloader = (furyutei_twitter_media_downloader.TwMediaDownloader(image_folder).process_directory(image_folder))

@router.get("/gallery/{hoga_id}")
def render_gallery(req: Request, hoga_id: int, db: Session = Depends(get_db)):
    requested_gallery = fetcher.fetch(hoga_id, db)
    return templates.TemplateResponse("render_gallery.html",
                                      context={
                                          "request": req,
                                          "requested_gallery": requested_gallery
                                      })


@router.get("/images/{filename}")
def get_image(filename: str, db: Session = Depends(get_db)):
    directory = db.query(Post).filter(Post.media_filenames.contains(filename)).first()
    if not directory:
        raise HTTPException(status_code=404, detail="Image not found")

    path = directory.media_filenames[filename]
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(path)


@router.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}
