from pathlib import Path
import re
from typing import Dict, List, NamedTuple
import hashlib

class MediaFile(NamedTuple):
    filename: str
    username: str
    id: str
    timestamp: str
    index: int
    extension: str

class GalleryDLExtractor:
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        if not self.directory_path.exists():
            raise ValueError(f"Directory does not exist: {directory_path}")
        # Generate a session ID for this scan
        self.session_id = hashlib.md5(str(self.directory_path).encode()).hexdigest()[:8]

    def parse_media_filename(self, filename: str) -> MediaFile:
        """Parse a media filename into its components."""
        pattern = r"(.+)-(\d+)-(\d+_\d+)-(\d+)\.(.+)"
        match = re.match(pattern, filename)
        if not match:
            raise ValueError(f"Invalid filename format: {filename}")

        username, id_str, timestamp, index, ext = match.groups()
        return MediaFile(
            filename=filename,
            username=username,
            id=id_str,
            timestamp=timestamp,
            index=int(index),
            extension=ext
        )
    def scan_directory(self) -> Dict[str, Dict]:
        """Scan directory and return organized post data."""
        result = {}

        # Get files in directory
        all_files = list(self.directory_path.glob("*"))
        metadata_files = list(self.directory_path.glob("metadata/*.json"))

        # Create metadata map
        metadata_map = {f.stem.split('_')[0]: f.name for f in metadata_files}

        # Process media files
        for file_path in all_files:
            if not file_path.is_file() or file_path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.mp4', '.gif'} or file_path.name.startswith('.'):
                continue

            try:
                parsed = self.parse_media_filename(file_path.name)

                if parsed.id not in result:
                    result[parsed.id] = {
                        'id': parsed.id,
                        'username': parsed.username,
                        'media_files': [],
                        'metadata_file': metadata_map.get(parsed.id),
                        'session_id': self.session_id,
                        '_base_dir': str(self.directory_path)  # Internal use only
                    }

                result[parsed.id]['media_files'].append(parsed.filename)

            except ValueError as e:
                print(f"Warning: Skipping file {file_path.name}: {e}")

        return result
