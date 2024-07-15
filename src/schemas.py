from typing import Dict, Optional

from pydantic import BaseModel


class DirectorySchema(BaseModel):
    hoga_id: int
    title: str
    extractor_type: None

    class Config:
        orm_mode = True


class BPost(BaseModel):
    post_id: int
    post_content: Optional[str]
    post_author_username: Optional[str]
    post_like_count: Optional[int]
    post_repost_count: Optional[int]
    media_filenames: Optional[Dict[str, str]]

    class Config:
        orm_mode = True