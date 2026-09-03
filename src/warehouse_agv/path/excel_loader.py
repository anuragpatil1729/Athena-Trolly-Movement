"""Load parametric path information from Excel."""

from pathlib import Path

import pandas as pd


def load_excel(path: str | Path):

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(
            f"Excel file not found: {path}"
        )

    return pd.read_excel(path)
