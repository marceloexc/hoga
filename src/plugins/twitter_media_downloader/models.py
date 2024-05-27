from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


@dataclass
class TwMediaDownloader_Tweet:
    tweet_date: datetime
    action_date: None
    display_name: str
    username: str
    tweet_url: str
    tweet_uuid: int
    media_type: str
    media_test_local_files: Dict
    remarks: str
    tweet_content: str
    number_of_replies: int
    number_of_retweets: int
    number_of_likes: int