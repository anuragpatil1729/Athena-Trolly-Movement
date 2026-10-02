#!/usr/bin/env python3

import sys
import time
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from warehouse_agv.sensors.potentiometer import Potentiometer


CONFIG_FILE = (
    PROJECT_ROOT
    / "config"
    / "sensors.yaml"
)


class MCP3008:

    def __init__(
        self,
        bus=0,
        device=0,
        speed=1_000_000,
    ):

        try:
            import spidev
        except ImportError as exc:
            raise RuntimeError(
                "spidev is required. "
                "Install it with: "
                "sudo apt install python3-spidev"
            ) from exc

        self.spi = spidev.SpiDev()

        self.spi.open(
            bus,
            device
        )

        self.spi.max_speed_hz = speed

    def read(self, channel):

        if not 0 <= channel <= 7:
            raise ValueError(
                "MCP3008 channel must be between 0 and 7."
            )

        result = self.spi.xfer2(
            [
                1,
                (8 + channel) << 4,
                0,
            ]
        )

        return (
            ((result[1] & 3) << 8)
            | result[2]
        )

    def close(self):
        self.spi.close()


def load_config():

    with CONFIG_FILE.open("r") as file:
        return yaml.safe_load(file)


def save_config(config):

    with CONFIG_FILE.open("w") as file:
        yaml.safe_dump(
            config,
            file,
            sort_keys=False,
            default_flow_style=False,
        )


def read_stable(adc, channel, samples=20):

    values = []

    for _ in range(samples):

        values.append(
            adc.read(channel)
        )

        time.sleep(0.02)

    return sum(values) / len(values)


def calibrate_sensor(
    adc,
    sensor_name,
    channel,
):

    raw_min = read_stable(
        adc,
        channel
    )

    angle_min = float(
        input(
            f"Enter physical angle at minimum "
            f"position for {sensor_name}: "
        )
    )

    raw_max = read_stable(
        adc,
        channel
    )

    angle_max = float(
        input(
            f"Enter physical angle at maximum "
            f"position for {sensor_name}: "
        )
    )

    if raw_min == raw_max:

        raise RuntimeError(
            f"{sensor_name}: ADC readings did not change."
        )

    converter = Potentiometer(
        raw_min=raw_min,
        raw_max=raw_max,
        angle_min=angle_min,
        angle_max=angle_max,
    )

    midpoint_raw = (
        raw_min + raw_max
    ) / 2.0

    converter.raw_to_angle(
        midpoint_raw
    )

    return (
        raw_min,
        raw_max,
        angle_min,
        angle_max,
    )


def main():

    config = load_config()

    adc = MCP3008()

    try:

        for index in range(1, 4):

            sensor_key = f"sensor_{index}"

            sensor = config[sensor_key]

            channel = sensor.get(
                "adc_channel"
            )

            if channel is None:

                channel = int(
                    input(
                        f"ADC channel for "
                        f"{sensor['name']}: "
                    )
                )

                sensor["adc_channel"] = channel

            result = calibrate_sensor(
                adc,
                sensor["name"],
                int(channel),
            )

            (
                raw_min,
                raw_max,
                angle_min,
                angle_max,
            ) = result

            sensor["raw_min"] = float(
                raw_min
            )

            sensor["raw_max"] = float(
                raw_max
            )

            sensor["angle_min_deg"] = (
                float(angle_min)
            )

            sensor["angle_max_deg"] = (
                float(angle_max)
            )

        save_config(config)

    finally:

        adc.close()


if __name__ == "__main__":
    main()