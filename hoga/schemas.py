from typing import Dict, Optional, List

from pydantic import BaseModel, HttpUrl


class DirectorySchema(BaseModel):
    hoga_id: int
    title: str
    extractor_type: None

    class Config:
        from_attributes = True


class BPost(BaseModel):
    post_id: int
    post_content: Optional[str]
    post_author_username: Optional[str]
    post_like_count: Optional[int]
    post_repost_count: Optional[int]
    media_filenames: Optional[Dict[str, str]]

    class Config:
        from_attributes = True


class GalleryResponse(BaseModel):
    gallery: List[BPost]

    class Config:
        from_attributes = True


class ImageResponseSchema(BaseModel):
    url: HttpUrl
    name: str