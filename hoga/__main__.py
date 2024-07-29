import sys

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from hoga.app import app


def main():
    uvicorn.run(app, host="0.0.0.0", port=5125, log_level="debug")


if __name__ == "__main__":
    main()
