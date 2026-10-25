
"""Route and time optimization for daily travel activities."""

from math import radians, sin, cos, asin, sqrt


def calculate_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Calculate straight-line distance between two coordinates."""
    earth_radius_km = 6371.0

    lat1, lon1, lat2, lon2 = map(
        radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    return 2 * earth_radius_km * asin(sqrt(min(1.0, a)))


def optimize_route(activities: list[dict]) -> list[dict]:
    """
    Arrange activities by nearest available coordinates.

    Activities without coordinates are kept after the
    coordinate-based activities, preserving their original order.
    """
    remaining = [
        (index, dict(activity))
        for index, activity in enumerate(activities)
    ]

    located = [
        item for item in remaining
        if item[1].get("latitude") is not None
        and item[1].get("longitude") is not None
    ]

    unlocated = [
        item for item in remaining
        if item[1].get("latitude") is None
        or item[1].get("longitude") is None
    ]

    if not located:
        return [activity for _, activity in remaining]

    ordered = [located.pop(0)]

    while located:
        current = ordered[-1][1]

        nearest_position = min(
            range(len(located)),
            key=lambda position: calculate_distance_km(
                current["latitude"],
                current["longitude"],
                located[position][1]["latitude"],
                located[position][1]["longitude"],
            ),
        )

        ordered.append(located.pop(nearest_position))

    result = [activity for _, activity in ordered]
    result.extend(activity for _, activity in unlocated)

    return result
