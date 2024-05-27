from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import User, Base, Directory, Post

import os

from src.plugins.twitter_media_downloader import furyutei_twitter_media_downloader, fetcher

app = FastAPI()

# create database columns
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


# database dependency, dunno how i feel about this being in main.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def get_index(req: Request, db: Session = Depends(get_db)):
    directories = db.query(Directory).all()
    return templates.TemplateResponse(
        "index.html",
        context={"request": req, "directories": directories}
    )

# this is how you do a post in fastapi. I have no idea what im reading
@app.post("/update", response_class=HTMLResponse)
def post_query(image_folder: str = Form(...)):
    downloader = (furyutei_twitter_media_downloader.TwMediaDownloader(image_folder).process_directory(image_folder))
    print(f'{image_folder} object created!')




@app.get("/gallery/{hoga_id}")
def render_gallery(req: Request, hoga_id:int, db: Session = Depends(get_db)):
    requested_gallery = fetcher.fetch(hoga_id, db)
    return templates.TemplateResponse("render_gallery.html",
                                      context={
                                          "request":req,
                                          "requested_gallery": requested_gallery
                                      })


@app.get("/images/{filename}")
def get_image(filename: str, db: Session = Depends(get_db)):
    directory = db.query(Post).filter(Post.media_filenames.contains(filename)).first()
    if not directory:
        raise HTTPException(status_code=404, detail="Image not found")

    path = directory.media_filenames[filename]
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(path)