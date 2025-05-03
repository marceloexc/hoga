import uvicorn

from hoga.app import app
import uvicorn

from hoga.app import app


def main():
    uvicorn.run("hoga.app:app", host="0.0.0.0", port=5125, log_level="debug", reload=True)


if __name__ == "__main__":
    main()
