from extractor import Extractor


class Twitter(Extractor):
    platform = "twitter"
    regex_identifier = [r"(?<!\d)\d{19}(?!\d)", r"^\d{19}$"]


#     make this into a dict?

