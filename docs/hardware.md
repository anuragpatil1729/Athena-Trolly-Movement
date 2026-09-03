# Hardware

## Main computer

Raspberry Pi running Ubuntu Linux.

## Drive

Two middle drive wheels.

Each drive wheel is connected to a motor.

## Motor driver

SmartElex 10D.

The SmartElex manual specifies two bidirectional brushed DC
motor channels using PWM and DIR.

Raspberry Pi mappings documented by the manual:

Motor 1:
PWM1 = GPIO12 / BCM32
DIR1 = GPIO24 / BCM18

Motor 2:
PWM2 = GPIO13 / BCM33
DIR2 = GPIO25 / BCM22

Verify the actual hardware wiring before enabling motor control.

## Sensors

Three passive sensor wheels are connected to potentiometers.

The Raspberry Pi requires an ADC to read analog potentiometer
signals.
