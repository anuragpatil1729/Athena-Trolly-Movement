#!/usr/bin/env python3

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from warehouse_agv.config.loader import load_yaml
from warehouse_agv.sensors.potentiometer import Potentiometer


SAMPLE_INTERVAL = 0.1


class MCP3008:

    def __init__(self, bus=0, device=0):

        try:
            import spidev
        except ImportError as exc:
            raise RuntimeError(
                "spidev is not installed. "
                "Install it with: "
                "sudo apt install python3-spidev"
            ) from exc

        self.spi = spidev.SpiDev()

        self.spi.open(
            bus,
            device
        )

        self.spi.max_speed_hz = 1_000_000

    def read(self, channel):

        if not 0 <= channel <= 7:
            raise ValueError(
                "MCP3008 channel must be 0-7."
            )

        response = self.spi.xfer2(
            [
                1,
                (8 + channel) << 4,
                0
            ]
        )

        value = (
            ((response[1] & 3) << 8)
            |
            response[2]
        )

        return value

    def close(self):

        self.spi.close()


def load_sensor_configuration():

    config_file = (
        PROJECT_ROOT
        / "config"
        / "sensors.yaml"
    )

    config = load_yaml(
        config_file
    )

    sensors = []

    for index in range(1, 4):

        sensor_config = config[
            f"sensor_{index}"
        ]

        channel = sensor_config.get(
            "adc_channel"
        )

        raw_min = sensor_config.get(
            "raw_min"
        )

        raw_max = sensor_config.get(
            "raw_max"
        )

        angle_min = sensor_config.get(
            "angle_min_deg"
        )

        angle_max = sensor_config.get(
            "angle_max_deg"
        )

        if None in (
            channel,
            raw_min,
            raw_max,
            angle_min,
            angle_max,
        ):

            raise RuntimeError(
                f"sensor_{index} is not fully "
                "configured in sensors.yaml."
            )

        sensors.append(
            {
                "name": sensor_config["name"],
                "channel": int(channel),
                "converter": Potentiometer(
                    raw_min=float(raw_min),
                    raw_max=float(raw_max),
                    angle_min=float(angle_min),
                    angle_max=float(angle_max),
                ),
            }
        )

    return sensors


def main():

    sensors = load_sensor_configuration()

    adc = MCP3008()

    try:

        while True:

            values = []

            for sensor in sensors:

                raw = adc.read(
                    sensor["channel"]
                )

                angle = sensor[
                    "converter"
                ].raw_to_angle(raw)

                values.append(
                    (
                        sensor["name"],
                        raw,
                        angle
                    )
                )

            print(
                "\n".join(
                    f"{name}: "
                    f"raw={raw:4d}, "
                    f"angle={angle:8.3f} deg"
                    for name, raw, angle in values
                )
            )

            print("-" * 50)

            time.sleep(
                SAMPLE_INTERVAL
            )

    except KeyboardInterrupt:
        pass

    finally:
        adc.close()


if __name__ == "__main__":
    main()