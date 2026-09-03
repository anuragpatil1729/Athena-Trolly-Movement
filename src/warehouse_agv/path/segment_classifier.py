"""Classify path segments."""


def classify_segment(curvature_values, tolerance=1e-6):

    if not curvature_values:

        return "unknown"

    if max(
        abs(value)
        for value in curvature_values
    ) <= tolerance:

        return "straight"

    return "curve"
