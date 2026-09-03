"""Safe mathematical parser for parametric equations."""

import sympy as sp


t = sp.symbols("t")


def parse_equation(expression: str):

    expression = expression.strip()

    expression = expression.replace(
        "np.cos",
        "cos"
    )

    expression = expression.replace(
        "np.sin",
        "sin"
    )

    expression = expression.replace(
        "np.tan",
        "tan"
    )

    expression = expression.replace(
        "np.sqrt",
        "sqrt"
    )

    allowed_functions = {

        "t": t,

        "cos": sp.cos,

        "sin": sp.sin,

        "tan": sp.tan,

        "sqrt": sp.sqrt,

        "pi": sp.pi,
    }

    return sp.sympify(
        expression,
        locals=allowed_functions
    )
