from pathlib import Path
import re
from flask import Flask
import json
import database
from typing import List
from data_structs import TwitterObjectHeader

MEDIA_EXTENSIONS = ['*.jpg', '*.png', '*.mp4', '*.jpeg']

app = Flask(__name__)

class Extractor:
    def __init__(self):
        self.platform = ""
        self.regex_identifier = ""

    def glob_files(self, root_path, extensions, pattern=None) -> List[str]:
        files_found = []
        for ext in extensions:
            files_found.extend(str(p) for p in Path(root_path).rglob(ext))
        if pattern:
            files_found = [f for f in files_found if pattern in Path(f).name]
        return files_found



    # these should go in their own sep util.py file

    def read_json_file(self, metadata_file_path):
        with open(metadata_file_path, 'r') as f:
            return json.load(f)

    def get_identifier_from_metadata_file(self, metadata_file_path) -> int:
        data = self.read_json_file(metadata_file_path)
        return data["tweet_id"]

    def get_media_count_from_metadata_file(self, metadata_file_path) -> int:
        data = self.read_json_file(metadata_file_path)
        return data["count"]

    def get_tweet_creation_date_from_metadata_file(self, metadata_file_path) -> str:
        data = self.read_json_file(metadata_file_path)
        return data["date"]


    # end util.py decl

    def return_regex_identifier(self, regex_identifier, input_string):

        match = re.search(regex_identifier, input_string)

        if match:
            return match.group()
        # make dict here by seeing if the metadata_file filename contains a part of the regex identifier
        # if not, discard it from the dictionary and don't add it
        # break this up as much as you need

        # TODO - replace this with try instead?

        # TODO - static?

    def make_dict(self, metadata_files):
        metadata_dict = {}

        for metadata_file in metadata_files:
            identifier = self.return_regex_identifier(
                self.regex_identifier, str(metadata_file)
            )
            if identifier:
                metadata_dict[identifier] = metadata_file

        return metadata_dict

    # currently at first i was using regex to get the pattern, but i dont need it since i already
    # have the string of the identifier from self.get_identifier_from_metadata_file, so to future me
    #please fix this

    def json_run(self, metadata_files, root_path):

        #TODO: is it better to pass it to a list and then make the db func parse it or should i just
        # let it take in one object at a time?
        twit_objs = []
        for file in metadata_files:
            try:
                tweet_date = self.get_tweet_creation_date_from_metadata_file(file)
                #### this is extremely wrong over here
            except:
                EnvironmentError #this is wrong
            #### ^^^ that was wrong
            if self.get_media_count_from_metadata_file(file) > 0:
                identifier_string = str(self.get_identifier_from_metadata_file(file))
                # bad var name! Only for tessting
                hello1 = self.glob_files(root_path,
                                      MEDIA_EXTENSIONS, pattern=identifier_string)
                twitter_obj = TwitterObjectHeader(identifier=identifier_string,
                                                  media_files=hello1,
                                                  date_created=tweet_date,
                                                  metadata_file=file)
                twit_objs.append(twitter_obj)
        self.insert_into_database(twit_objs)




    def insert_into_database(self, twitter_objects):
        with app.app_context():
            db = database.get_db()
            cur = db.cursor()
            for twitter_object in twitter_objects:
                cur.execute('''
                        INSERT OR REPLACE INTO 
                        metadata_table(identifier, date, file_path, media) 
                        VALUES (?, ?, ?, ?)
                        ''',
                        (twitter_object.identifier,
                         twitter_object.date_created,
                         str(twitter_object.metadata_file), str(twitter_object.media_files)))
            db.commit()
