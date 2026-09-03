#!/usr/bin/env python3

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src")
)

from warehouse_agv.path.excel_loader import (
    load_excel
)


EXCEL = (
    PROJECT_ROOT /
    "data/raw/AGV Turn Dynamics Excel.xlsx"
)


def main():

    if not EXCEL.exists():

        print(
            f"Excel file not found:\n{EXCEL}"
        )

        print(
            "\nCopy your Excel workbook into:"
        )

        print(
            "data/raw/"
        )

        return 1

    dataframe = load_excel(
        EXCEL
    )

    print("\n================================")
    print(" Excel Inspection")
    print("================================")

    print(
        f"\nRows: {len(dataframe)}"
    )

    print(
        f"Columns: {list(dataframe.columns)}"
    )

    print("\nFirst rows:\n")

    print(
        dataframe.head()
    )

    return 0


if __name__ == "__main__":

    raise SystemExit(
        main()
    )
