import sys

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from src.app import app

from typing import Any, Dict

import logging

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5125, log_level="debug")
