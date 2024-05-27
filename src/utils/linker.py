import os
class MediaLinker:

    def __init__(self, working_directory):
        self.working_directory = working_directory

    def link_media(self, media_filename):
        for root, dirs, files in os.walk(self.working_directory):
            if media_filename in files:
                full_path = os.path.abspath(os.path.join(root, media_filename))
                return {media_filename: full_path}
