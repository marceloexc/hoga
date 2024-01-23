from pathlib import Path
import re
from flask import Flask
import database
app = Flask(__name__)

class Extractor:
    def __init__(self):
        self.platform = ""
        self.regex_identifier = ""

    # TODO - https://stackoverflow.com/questions/47655205/pathlib-path-glob-and-multiple-file-extension
    def glob_files(self, root_path, extensions):
        files_found = []
        for ext in extensions:
            files_found.extend(Path(root_path).rglob(ext))
        print(files_found)
        return files_found

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

    def insert_into_database(self, metadata_dict):
        with app.app_context():
            db = database.get_db()
            cur = db.cursor()
            for identifier, file_path in metadata_dict.items():
                print(identifier, str(file_path))
                cur.execute('''
                            INSERT INTO metadata_table(identifier, file_path) VALUES (?, ?)
                            ''',
                            (identifier, str(file_path)))
            db.commit()

