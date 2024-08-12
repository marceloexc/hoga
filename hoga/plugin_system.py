from typing import Optional, DefaultDict, Dict

from sqlmodel import Field, SQLModel

from datetime import datetime


class GenericPostModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    plaintext_content: str
    originating_platform: str
    originating_author: str
    originating_id: str
    published_date: datetime = Field(default_factory=datetime.utcnow)
    media_mapping: Optional[DefaultDict[str, str]]

    engagements: Optional[Dict[str]]
