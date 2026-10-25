from datetime import timedelta

from models import Activity, DayPlan, Itinerary, TripRequest

THEME_ROTATION = [
    ("culture", "Local landmarks and neighborhood walks"),
    ("food", "Markets, cafes, and regional dishes"),
    ("nature", "Parks, viewpoints, and outdoor time"),
    ("adventure", "Active experiences and hidden spots"),
    ("relaxation", "Slow morning and scenic evening"),
    ("history", "Museums and historic streets"),
    ("shopping", "Boutiques, crafts, and souvenirs"),
    ("nightlife", "Evening streets, live music, and local hangouts"),
]

TIPS = [
    "Keep 10-15% of the budget for snacks, transit, and small surprises.",
    "Book the most popular attraction for the first or second morning.",
    "Leave one afternoon lightly planned in case weather or energy changes.",
    "Save restaurant names, but choose based on what looks busy with locals.",
]


def _pick_theme(interests: list[str], index: int) -> tuple[str, str]:
    preferred = [item for item in THEME_ROTATION if item[0] in interests]
    pool = preferred or THEME_ROTATION
    return pool[index % len(pool)]


def build_sample_itinerary(trip: TripRequest) -> Itinerary:
    """Build a readable day-by-day plan without calling an AI API."""
    daily_budget = round(trip.budget / trip.trip_days, 2)
    days: list[DayPlan] = []

    for index in range(trip.trip_days):
        current_date = trip.start_date + timedelta(days=index)
        interest, theme = _pick_theme(trip.interests, index)
        day_number = index + 1
        is_first = index == 0
        is_last = index == trip.trip_days - 1

        morning_title = (
            f"Arrive and settle in {trip.destination}"
            if is_first
            else f"Morning {interest} plan in {trip.destination}"
        )
        evening_title = (
            f"Farewell evening in {trip.destination}"
            if is_last
            else f"Evening {interest} highlight"
        )
        meal_cost = round(daily_budget * 0.28, 2)
        activity_cost = round(daily_budget * 0.35, 2)
        evening_cost = round(daily_budget * 0.22, 2)

        days.append(
            DayPlan(
                day=day_number,
                date=current_date.isoformat(),
                theme=theme,
                summary=(
                    f"Day {day_number} mixes {interest} with easy pacing so the "
                    f"${daily_budget:,.0f} daily budget stays realistic."
                ),
                activities=[
                    Activity(
                        time="Morning",
                        title=morning_title,
                        description=(
                            "Start with a neighborhood walk, a landmark nearby, "
                            "and a simple local breakfast."
                            if is_first
                            else f"Visit a well-known {interest} stop and a quieter nearby street."
                        ),
                        estimated_cost=activity_cost if not is_first else round(daily_budget * 0.18, 2),
                    ),
                    Activity(
                        time="Afternoon",
                        title=f"{interest.title()} lunch and a second stop",
                        description=(
                            f"Choose a mid-range restaurant that matches your {interest} "
                            "interest, then add one museum, market, park, or viewpoint."
                        ),
                        estimated_cost=meal_cost,
                    ),
                    Activity(
                        time="Evening",
                        title=evening_title,
                        description=(
                            "Keep dinner and transit simple, then use leftover budget "
                            "for a dessert, viewpoint, or short live-music stop."
                        ),
                        estimated_cost=evening_cost,
                    ),
                ],
            )
        )

    return Itinerary(
        destination=trip.destination,
        start_date=trip.start_date.isoformat(),
        end_date=trip.end_date.isoformat(),
        budget=trip.budget,
        interests=trip.interests,
        trip_days=trip.trip_days,
        daily_budget=daily_budget,
        source="sample",
        days=days,
        tips=TIPS,
        saved=False,
    )
