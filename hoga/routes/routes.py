import logging
import os
from pathlib import Path

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session

from hoga.database import get_db
from hoga.models import Directory, Post
from ..plugins.plugin_gallerydl import gallerydlplugin
from ..plugins.twitter_media_downloader import furyutei_twitter_media_downloader
from hoga.gallery import fetcher
from hoga.shared import templates

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


# In-memory store of session -> directory mapping
SESSION_DIRS = {}

@router.get("/image2/{session_id}/{filename}")
def get_image2(session_id: str, filename: str):
    if session_id not in SESSION_DIRS:
        raise HTTPException(status_code=404, detail="Invalid session")

    base_dir = SESSION_DIRS[session_id]
    file_path = Path(base_dir) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(str(file_path))

@router.post("/gallerydl_gallery", response_class=HTMLResponse)
def add_folder_to_queue(image_folder: str = Form(...)):
    """Process a gallery-dl folder and return organized post information."""
    try:
        extractor = gallerydlplugin.GalleryDLExtractor(image_folder)
        posts = extractor.scan_directory()

        # Store session mapping
        SESSION_DIRS[extractor.session_id] = image_folder

        # Create HTML response
        html_content = "<h2>Processed Gallery Posts</h2>"

        for post_id, post_data in posts.items():
            html_content += f"""
            <div style='margin-bottom: 20px; padding: 10px; border: 1px solid #ccc;'>
                <h3>Post ID: {post_data['id']}</h3>
                <p>Username: {post_data['username']}</p>
                <p>Media Files:</p>
                <div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px;'>
                """

            session_id = post_data['session_id']
            for file in sorted(post_data['media_files']):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    html_content += f"""
                    <div style='text-align: center;'>
                        <img src="/image2/{session_id}/{file}" style='max-width: 100%; height: auto; margin-bottom: 5px;'>
                        <div style='font-size: 0.8em; word-break: break-all;'>{file}</div>
                    </div>
                    """
                else:
                    html_content += f"""
                    <div style='text-align: center;'>
                        <div style='padding: 20px; background: #f0f0f0; margin-bottom: 5px;'>{file}</div>
                        <div style='font-size: 0.8em; word-break: break-all;'>{file}</div>
                    </div>
                    """

            html_content += f"""
                </div>
                {f"<p>Metadata: {post_data['metadata_file']}</p>" if post_data['metadata_file'] else "<p>No metadata file</p>"}
            </div>
            """

        return HTMLResponse(content=html_content)

    except Exception as e:
        return HTMLResponse(content=f"<h2>Error</h2><p>Error processing directory: {str(e)}</p>")

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
