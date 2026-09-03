from warehouse_agv.control.pid import PID


def test_pid_zero_error():

    controller = PID(
        1.0,
        0.0,
        0.0
    )

    output = controller.update(
        0.0,
        0.1
    )

    assert output == 0.0
