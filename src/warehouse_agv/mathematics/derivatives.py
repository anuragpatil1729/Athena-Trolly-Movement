"""Parametric equation derivatives."""

import sympy as sp


def derivatives(x_expr, y_expr, parameter):

    dx = sp.diff(
        x_expr,
        parameter
    )

    dy = sp.diff(
        y_expr,
        parameter
    )

    ddx = sp.diff(
        dx,
        parameter
    )

    ddy = sp.diff(
        dy,
        parameter
    )

    return dx, dy, ddx, ddy
