
from datetime import date, timedelta

from app.services.route_optimizer import optimize_route


def build_daily_itinerary(
    destination: str,
    start_date: str,
    end_date: str,
    interests: list[str],
    travel_pace: str = "balanced",
) -> list[dict]:
    """Build a structured day-by-day itinerary."""

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    if end < start:
        raise ValueError("End date must be on or after start date.")

    if (end - start).days > 13:
        raise ValueError("Trip must be 14 days or fewer.")

    if not destination.strip():
        raise ValueError("Destination cannot be empty.")

    interests = interests or ["sightseeing"]

    activities_per_day = {
        "relaxed": 2,
        "balanced": 3,
        "packed": 4,
    }.get(travel_pace, 3)

    itinerary = []
    current = start
    day_number = 1

    while current <= end:
        activities = []

        time_slots = ["Morning", "Afternoon", "Evening", "Night"]
        suggestions = [
            f"Explore a popular attraction in {destination}",
            f"Discover local {interests[0]} experiences in {destination}",
            "Enjoy a local meal and explore the neighbourhood",
            f"Take an optional evening walk in {destination}",
        ]

        for index in range(activities_per_day):
            activities.append({
                "time": time_slots[index],
                "title": suggestions[index],
                "description": (
                    f"Choose a suitable {destination} experience "
                    "that matches your interests and available time."
                ),
                "estimated_cost": 0,
            })

        optimized_activities = optimize_route(activities)

        itinerary.append({
            "day": day_number,
            "date": current.isoformat(),
            "theme": (
                f"{interests[(day_number - 1) % len(interests)].title()} "
                "and exploration"
            ),
            "summary": (
                f"Day {day_number} of your trip to {destination}, "
                f"planned at a {travel_pace} pace with route optimization."
            ),
            "activities": optimized_activities,
        })

        current += timedelta(days=1)
        day_number += 1

    return itinerary

