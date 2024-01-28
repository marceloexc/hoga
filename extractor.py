from pathlib import Path
import re
from flask import Flask
import json
import database
from typing import List

MEDIA_EXTENSIONS = ['*.jpg', '*.png', '*.mp4', '*.jpeg']

app = Flask(__name__)

class Extractor:
    def __init__(self):
        self.platform = ""
        self.regex_identifier = ""

    def glob_files(self, root_path, extensions, pattern=None) -> List[None]:
        files_found = []
        for ext in extensions:
            files_found.extend(Path(root_path).rglob(ext))
        if pattern:
            files_found = [f for f in files_found if pattern in f.name]
        return files_found

    def read_json_file(self, metadata_file_path):
        with open(metadata_file_path, 'r') as f:
            return json.load(f)

    def get_identifier_from_metadata_file(self, metadata_file_path) -> int:
        data = self.read_json_file(metadata_file_path)
        return data["tweet_id"]

    def get_media_count_from_metadata_file(self, metadata_file_path) -> int:
        data = self.read_json_file(metadata_file_path)
        return data["count"]


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

    def json_run(self, metadata_files, root_path, pattern1):
        for file in metadata_files:
            if self.get_media_count_from_metadata_file(file) > 0:
                identifier_string = str(self.get_identifier_from_metadata_file(file))
                # bad var name! Only for tessting
                hello1 = self.glob_files(root_path,
                                      MEDIA_EXTENSIONS, pattern=identifier_string)
                print(file, len(hello1))

    def insert_into_database(self, metadata_dict):
        with app.app_context():
            db = database.get_db()
            cur = db.cursor()
            for identifier, file_path in metadata_dict.items():
                cur.execute('''
                            INSERT OR REPLACE INTO metadata_table(identifier, file_path) VALUES (?, ?)
                            ''',
                            (identifier, str(file_path)))
            db.commit()
