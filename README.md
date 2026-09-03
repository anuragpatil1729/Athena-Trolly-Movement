# Warehouse AGV

Warehouse trolley/AGV controller running on Raspberry Pi
with Ubuntu Linux and Python.

## System

- Warehouse represented by nodes.
- Existing Excel workbook contains predefined parametric paths.
- Path represented by x(t), y(t).
- Two middle wheels are the drive wheels.
- Three additional wheels are connected to potentiometers.
- Potentiometers are used for straight-path deflection correction.
- SmartElex 10D controls the two drive motors.

## Architecture

Target Node
    ↓
Route Planner
    ↓
Parametric Path
    ↓
Straight / Curve Controller
    ↓
Two Drive Wheels
    ↓
SmartElex 10D
    ↓
Drive Motors

Straight:
    Path geometry
        +
    3 potentiometer measurements
        ↓
    Deflection correction
        ↓
    PID

Curve:
    x(t), y(t)
        ↓
    Curvature
        ↓
    Wheel speed calculation

## Development order

1. Inspect Excel workbook.
2. Map nodes and path segments.
3. Parse x(t), y(t).
4. Plot complete warehouse path.
5. Verify mathematical continuity.
6. Implement node-to-node navigation.
7. Calibrate potentiometers.
8. Implement straight-line deflection control.
9. Implement curve controller.
10. Test SmartElex and motors.
11. Run simulation.
12. Low-speed physical testing.
