# setup.py
from setuptools import setup, find_packages

setup(
    name="hoga",
    version="0.0.1",
    description="extensible and self hosted viewer for archived social media content",
    url="https://github.com/marceloexc/hoga",
    author="marceloexc",
    license="GPLv3",
    packages=find_packages(),
    # packages=find_packages(where="hoga",exclude=["hoga.egg_info",]),
    # package_dir={"": "hoga"},
    install_requires=[
        "fastapi-slim~=0.111.0",
        "SQLAlchemy~=2.0.30",
        "uvicorn~=0.29.0",
        "sqlmodel~=0.0.19",
        "pydantic~=2.7.1",
        "libsass~=0.23.0",
        "Jinja2~=3.1.4",
        "python-multipart~=0.0.9"
    ],
    entry_points={
        "console_scripts": [
            "hoga = hoga.__main__:main",
        ],
    },

)
