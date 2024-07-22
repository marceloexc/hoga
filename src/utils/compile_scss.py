import sass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

CURRENT_PATH = Path(__file__).parent

COMPILED_DIR = (CURRENT_PATH / '../static/styles').resolve()
SCSS_DIR = (CURRENT_PATH / '../static/sass').resolve()


def compile_scss():
    sass.compile(dirname=(str(SCSS_DIR), str(COMPILED_DIR)), output_style="nested")
    logger.info("Compiled scss -> css")


if __name__ == "__main__":
    compile_scss()
