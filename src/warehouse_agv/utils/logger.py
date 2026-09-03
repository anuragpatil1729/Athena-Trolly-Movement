"""Logging setup."""

import logging


def get_logger(
    name="warehouse_agv"
):

    return logging.getLogger(
        name
    )
