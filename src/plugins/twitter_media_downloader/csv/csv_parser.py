import os
from datetime import datetime

from src.plugins.twitter_media_downloader.models import TwMediaDownloader_Tweet
from src.utils.csv_processor import CSVFileHandler
from src.utils.linker import MediaLinker

class TweetRow:

    # Normal TwMediaDownloader CSV File:
    # Column 1: Tweet Date (in the form 2023/02/08 05:58:23)
    # Column 2: Action Date (only applicable for retweets)
    # Column 3: Display name
    # Column 4: Username with @
    # Column 5: Tweet URL
    # Column 6: Media Type (Image, GIF, Video)
    # Column 7: Media URL (if applicable)
    # Column 8: Saved Filename on disk
    # Column 9: Remarks (?)
    # Column 10: Tweet content. Includes URL to media if the original status had it
    # Column 11: Reply count
    # Column 12: Retweet count
    # Column 13: Like count

    def __init__(self, row, file_path):
        self.row = row
        self.file_path = file_path

    @property
    def tweet_creation_date_cell(self):
        return datetime.strptime(self.row[0], '%Y/%m/%d %H:%M:%S')

    @property
    def tweet_action_date_cell(self):
        return None if self.row[1] == '' else datetime.strptime(self.row[1], '%Y/%m/%d %H:%M:%S')

    @property
    def tweet_display_name_cell(self):
        return self.row[2]

    @property
    def tweet_username_cell(self):
        return self.row[3]

    @property
    def tweet_url_cell(self):
        return self.row[4]

    @property
    def tweet_media_type_cell(self):
        return self.row[5]

    @property
    def tweet_media_path_locally_cell(self):

        directory_path = os.path.dirname(self.file_path)

        media_url = MediaLinker(directory_path)
        # this is the part where we will have to invoke the media linker

        image_map = media_url.link_media(self.row[7])

        return image_map

    @property
    def tweet_content_cell(self):
        return self.row[9]

    @property
    def tweet_reply_count(self):
        # return int(self.row[12])
        return 12
    @property
    def tweet_retweet_count(self):
        if self.row[11].isdigit():
            return int(self.row[11])
        else:
            return 0

    @property
    def tweet_favorite_count(self):
        if self.row[12].isdigit():
            return int(self.row[12])
        else:
            return 0

    @property
    def tweet_status_uuid(self):
        tweet_status_string = self.row[4].split("status/")[-1]

        return int(tweet_status_string)


class TwMediaDownloaderCSVProcessor(CSVFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.CSV_HEADER_SKIP = 6


    def create_tweet_objects(self):
        if self.csv_data is None:
            self.read_file()  # Read the file if data is not already loaded

        tweet_objects = {}
        for row in self.csv_data.rows:
            tweet_row = TweetRow(row, self.file_path)
            current_tweet_uuid_in_row = tweet_row.tweet_status_uuid
            # If a tweet object with the same uuid already exists, append the new filename
            if current_tweet_uuid_in_row in tweet_objects:

                # worst piece of shit unreadable code ive ever written. Sorry to future me. This wont be how
                # the plugin system works at all...promise...
                tweet_objects[current_tweet_uuid_in_row].media_test_local_files.update(MediaLinker(os.path.dirname(self.file_path)).link_media(tweet_row.row[7]))
            else:
                # If it doesn't exist, create a new tweet object
                tweet_objects[current_tweet_uuid_in_row] = self.create_tweet_object(tweet_row)

        return tweet_objects.values()
    def create_tweet_object(self, tweet_row):
        return TwMediaDownloader_Tweet(
            tweet_date=tweet_row.tweet_creation_date_cell,
            action_date=tweet_row.tweet_action_date_cell,
            display_name=tweet_row.tweet_display_name_cell,
            username=tweet_row.tweet_username_cell,
            tweet_url=tweet_row.tweet_url_cell,
            tweet_uuid=tweet_row.tweet_status_uuid,
            media_type=tweet_row.tweet_media_type_cell,
            media_test_local_files= tweet_row.tweet_media_path_locally_cell, # This is now a list
            tweet_content=tweet_row.tweet_content_cell,
            number_of_replies=tweet_row.tweet_reply_count,
            number_of_retweets=tweet_row.tweet_retweet_count,
            remarks="string",
            number_of_likes=tweet_row.tweet_favorite_count
        )



