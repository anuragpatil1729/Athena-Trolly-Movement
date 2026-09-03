# Mathematics

For a parametric path:

x = x(t)
y = y(t)

The tangent is obtained from:

dx/dt
dy/dt

Heading:

theta = atan2(dy/dt, dx/dt)

Curvature:

kappa =
(x' y'' - y' x'') /
(x'^2 + y'^2)^(3/2)

For a two-wheel drive system:

v_left =
v - (L/2) omega

v_right =
v + (L/2) omega

where L is the distance between the drive wheels.

For a curve:

omega = v * kappa

The exact physical units and robot dimensions must be
configured from measurements.
