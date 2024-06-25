import sys

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from src.app import app

from typing import Any, Dict

import logging

if __name__ == "__main__":
    # https://github.com/tiangolo/fastapi/discussions/7457

    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    # stream_handler = logging.StreamHandler(sys.stdout)
    # log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # stream_handler.setFormatter(log_formatter)
    # logger.addHandler(stream_handler)
    #
    # logger.info(
    #     'API is starting up')  #https://stackoverflow.com/questions/77001129/how-to-configure-fastapi-logging-so-that-it-works-both-with-uvicorn-locally-and

    uvicorn.run(app, host="0.0.0.0", port=5125, log_level="debug")
