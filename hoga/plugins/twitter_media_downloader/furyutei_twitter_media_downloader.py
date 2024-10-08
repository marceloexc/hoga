import random

import logging
from hoga.models import Post, Directory
from ...plugins.twitter_media_downloader.csv.csv_parser import TwMediaDownloaderCSVProcessor

import os

from hoga.database import SessionLocal

logger = logging.getLogger(__name__)

class TwMediaDownloader:
    def __init__(self, directory_path, file_extension='.csv'):
        self.FILE_EXTENSION = file_extension
        self.DIRECTORY_PATH = directory_path
        self.file_paths = []

    def process_directory(self, directory_path):
        logger.info(f"Using TwMediaDownloader at {directory_path}")

        if not os.path.exists(directory_path):
            # logger.debug("Aborting - directory does not exist!")
            return

        for file in os.listdir(directory_path):
            if file.endswith(self.FILE_EXTENSION):
                absolute_path = os.path.join(directory_path, file)
                self.file_paths.append(absolute_path)

        for file_path in self.file_paths:
            processor = TwMediaDownloaderCSVProcessor(file_path)
            processor.read_file()
            tweets = processor.create_tweet_objects()
            self.commit_to_db(tweets)

    def commit_to_db(self, tweets):
        session = SessionLocal()
        try:
            directory_entry = Directory(
                hoga_id=random.randint(1, 1000000),  # Generate a random integer ID
                title=self.DIRECTORY_PATH  # Use the directory name as the title
            )
            session.add(directory_entry)
            session.commit()

            for tweet in tweets:
                tweet_post = Post(
                    post_id=tweet.tweet_uuid,
                    post_author_username=tweet.username,
                    post_author_handle=tweet.display_name,
                    media_filenames=tweet.media_test_local_files,
                    directory_id=directory_entry.hoga_id,
                    post_content=tweet.tweet_content,
                    post_like_count=tweet.number_of_likes,
                    post_repost_count=tweet.number_of_retweets
                )
                session.add(tweet_post)
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"An error occured: {e}")
        finally:
            logger.info(f"Finished processing gallery at {self.DIRECTORY_PATH}")
            session.close()
