from sqlalchemy.orm import Session
from src.models import Post

def fetch(hoga_id, db: Session):
    all_posts = db.query(Post).filter_by(directory_id = hoga_id).all()
    return all_posts