from extractor import Extractor


class Twitter(Extractor):
    def __init__(self):
        super().__init__()
        self.platform = "twitter"
        self.regex_identifier = r"(?<!\d)\d{19}(?!\d)"
