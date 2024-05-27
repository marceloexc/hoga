# models.py

from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Directory(Base):
    __tablename__ = "directories"

    hoga_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)
    extractor_type = Column(String(50), nullable=True)
    posts = relationship('Post', backref="directory", lazy='selectin')


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    media_filenames = Column(JSON, nullable=True)
    post_content = Column(String(900), nullable=True)
    post_type = Column(String(30), nullable=True)
    post_platform = Column(String(30), nullable=True)
    post_published_timestamp = Column(String(30), nullable=True)
    post_author_handle = Column(String(30), nullable=True)
    post_author_username = Column(String(30), nullable=True)
    post_repost_id = Column(String(30), nullable=True)
    post_media_attachments = Column(String(30), nullable=True)
    post_like_count = Column(String(30), nullable=True)
    post_repost_count = Column(String(30), nullable=True)
    post_bookmark_count = Column(String(30), nullable=True)
    post_comments_count = Column(String(30), nullable=True)
    repost_original_post_id = Column(String(30), nullable=True)
    post_privacy_settings = Column(String(30), nullable=True)
    directory_id = Column(Integer, ForeignKey('directories.hoga_id'), nullable=False)

    # post_date = Column(DATETIME )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)