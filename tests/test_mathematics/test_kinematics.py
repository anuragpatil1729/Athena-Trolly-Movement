from warehouse_agv.mathematics.wheel_kinematics import (
    wheel_speeds
)


def test_straight_motion():

    left, right = wheel_speeds(
        1.0,
        0.0,
        0.5
    )

    assert left == right
