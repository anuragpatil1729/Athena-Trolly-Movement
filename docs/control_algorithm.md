# Control Algorithm

## Straight path

The predefined path identifies a straight segment.

The three potentiometer wheels provide deflection measurements.

The measurements are converted to a deflection error.

A PID controller generates a correction.

The correction modifies the two drive-wheel speeds.

## Curve

The predefined x(t), y(t) equations define the curve.

The mathematical path is used to calculate curvature.

Curvature is converted into angular velocity and then
into left/right drive-wheel velocities.
