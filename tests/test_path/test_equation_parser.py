from warehouse_agv.path.equation_parser import parse_equation


def test_linear_equation():

    expression = parse_equation(
        "100 + 50*t"
    )

    assert expression is not None
