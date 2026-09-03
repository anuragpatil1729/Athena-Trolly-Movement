"""Sample a parametric path."""

import numpy as np


def sample_parameter(
    t_start: float,
    t_end: float,
    samples: int = 100,
):

    return np.linspace(
        t_start,
        t_end,
        samples
    )
