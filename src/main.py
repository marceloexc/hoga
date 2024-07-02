import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from src.app import app

if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:5125"]
    config.loglevel = "debug"

    asyncio.run(serve(app, config))