from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any

from sqlmodel import SQLModel, Session


class Plugin(ABC):
    """Base class for Plugins"""

    name = None
    description = ""

    def __init__(self, directory: Path, db_session: Session):
        self.directory = directory
        self.db_session = db_session

    @abstractmethod
    def scan(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def fetch_media(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def commit_to_db(self, data: Dict[str, Any]) -> SQLModel:
        pass

    @abstractmethod
    def render_content(self, data: SQLModel) -> str:
        pass

