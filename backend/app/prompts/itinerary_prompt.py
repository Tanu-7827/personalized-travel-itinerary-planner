
from typing import Optional


def build_itinerary_prompt(
    destination: str,
    start_date: str,
    end_date: str,
    travel_style: str = "cultural",
    interests: Optional[list[str]] = None,
    group_size: int = 1,
    pace: str = "moderate",
    budget_per_day: float = 100.0,
    dietary_restrictions: Optional[list[str]] = None,
    mobility_concerns: Optional[str] = None,
) -> str:
    """Build a personalized prompt for AI itinerary generation."""

    interests = interests or []
    dietary_restrictions = dietary_restrictions or []

    pace_description = {
        "relaxed": "one or two main activities per day with plenty of rest",
        "moderate": "two to three main activities per day with some downtime",
        "fast": "three to four main activities per day",
    }.get(pace.lower(), "two to three main activities per day")

    dietary_info = (
        ", ".join(dietary_restrictions)
        if dietary_restrictions
        else "No special dietary requirements"
    )

    mobility_info = (
        mobility_concerns
        if mobility_concerns
        else "No specific mobility concerns provided"
    )

    interests_text = ", ".join(interests) if interests else "General sightseeing"

    prompt = f"""
You are an experienced travel itinerary planner.

Create a personalized day-by-day itinerary with these details:

Destination: {destination}
Start date: {start_date}
End date: {end_date}
Travel style: {travel_style}
Interests: {interests_text}
Number of travellers: {group_size}
Travel pace: {pace}
Daily budget: ${budget_per_day:.2f}
Dietary requirements: {dietary_info}
Mobility considerations: {mobility_info}

Instructions:
1. Organize activities by date and morning, afternoon, and evening.
2. Match activities to the traveler's interests and travel style.
3. Follow the requested pace: {pace_description}.
4. Keep estimated daily costs within the daily budget.
5. Consider dietary and mobility requirements.
6. Include practical transport and travel tips.
7. Avoid inventing opening hours, prices, or availability.
8. Make the itinerary clear, realistic, and easy to follow.

Return the itinerary in a structured format suitable for the application.
"""

    return prompt.strip()
