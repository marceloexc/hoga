from dataclasses import dataclass, field

#order=True necessary?
@dataclass(frozen=True, order=True)
class TwitterObjectHeader:
    identifier: int
    tweet_text_content: str = ""
    date_created: str = ""
    metadata_file: str = ""
    media_files: list[str] = field(default_factory=list)