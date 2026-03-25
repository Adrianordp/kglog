"""
Module to get the version of the application from pyproject.toml
"""

import tomllib
from importlib.resources import files


def get_version() -> str:
    pyproject_path = files("app").joinpath("..", "pyproject.toml")

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    return data["project"]["version"]
