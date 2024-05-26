from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import database, models
from .plugins.twitter_media_downloader import furyutei_twitter_media_downloader

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.on_event("startup")
async def on_startup():
    await database.init_db()

# Dependency to get DB session
async def get_db():
    async with database.SessionLocal() as session:
        yield session

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Directory))
    directories = result.scalars().all()
    return templates.TemplateResponse("index.html", {"request": request, "directories": directories})

@app.post("/", response_class=HTMLResponse)
async def post_index(request: Request, image_folder: str = Form(...), db: AsyncSession = Depends(get_db)):
    print("MY IMAGE FOLDER " + image_folder)
    downloader = furyutei_twitter_media_downloader.TwMediaDownloader(image_folder, db)
    await downloader.process_directory(image_folder)
    return templates.TemplateResponse("index.html", {"request": request, "user": downloader})

# Define the render_gallery route
@app.get("/gallery/{hoga_id}", response_class=HTMLResponse)
async def render_gallery(request: Request, hoga_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Directory).filter(models.Directory.hoga_id == hoga_id))
    directory = result.scalars().first()
    if directory is None:
        return HTMLResponse(status_code=404, content="Directory not found")
    return templates.TemplateResponse("gallery.html", {"request": request, "directory": directory})
