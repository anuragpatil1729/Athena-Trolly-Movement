"""Configuration loader."""

from pathlib import Path

import yaml


def load_yaml(path: str | Path) -> dict:

    path = Path(path)

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
