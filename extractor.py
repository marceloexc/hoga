from pathlib import Path
import re


class Extractor:
    platform = ""
    regex_identifier = []

    @classmethod
    def retrieve_files(cls, root_directory_path):
        directory_path = Path(root_directory_path)
        json_files_list = cls.find_json_files(directory_path)
        media_dict = cls.find_matching_media(directory_path, json_files_list)
        return media_dict

    @classmethod
    def iterate_files(cls, directory_path):
        for file_path in directory_path.rglob("[!.]*"):
            yield file_path

    @classmethod
    def find_json_files(cls, directory_path):
        json_files = []
        for file_path in cls.iterate_files(directory_path):
            if (
                    file_path.is_file()
                    and file_path.suffix == ".json"
                    and any(
                re.search(pattern, file_path.name)
                for pattern in cls.regex_identifier
            )
            ):
                json_files.append(file_path)
        return json_files

    @classmethod
    def find_matching_media(cls, directory_path, json_list):
        media_dict = {}
        for file_path in cls.iterate_files(directory_path):
            if file_path.is_file() and file_path.suffix != ".json":
                identifier = cls.return_regex_identifier(
                    cls.regex_identifier, str(file_path)
                )
                # Check if the identifier matches any JSON file stems
                for json_file in json_list:
                    if (
                            json_file is not None
                            and json_file.suffix == ".json"
                            and identifier in json_file.stem
                    ):
                        # Find the corresponding JSON file path
                        media_dict.setdefault(str(json_file), []).append(file_path)

        return media_dict

    # todo : what is __iter__ ?

    # todo: currently availability of media files dictates control of json_file, this means that if the tweet is only
    # text based, then it doessnt show up in the list. change it so that json_files get caught first and then from there
    # we can start to get text based tweets

    @classmethod
    def return_regex_identifier(cls, regex_identifier, input_string):
        match = re.search(regex_identifier[0], input_string)

        if match:
            return match.group()
