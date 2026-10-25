from app.prompts.itinerary_prompt import build_itinerary_prompt
import json

from datetime import timedelta

import httpx

from config import Settings
from models import Activity, DayPlan, Itinerary, TripRequest
from sample_itinerary import build_sample_itinerary

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def _fallback_days(trip: TripRequest, parsed: dict) -> list[DayPlan]:
    sample = build_sample_itinerary(trip)
    sample_days = {day.day: day for day in sample.days}
    days: list[DayPlan] = []
    raw_days = parsed.get("days") or []

    for index in range(trip.trip_days):
        current = trip.start_date + timedelta(days=index)
        raw = raw_days[index] if index < len(raw_days) and isinstance(raw_days[index], dict) else {}
        fallback = sample_days[index + 1]
        activities = []
        for activity in raw.get("activities") or []:
            if not isinstance(activity, dict):
                continue
            activities.append(
                Activity(
                    time=str(activity.get("time") or "Anytime")[:20],
                    title=str(activity.get("title") or "Local activity")[:80],
                    description=str(activity.get("description") or "Explore the area.")[:280],
                    estimated_cost=max(float(activity.get("estimated_cost") or 0), 0),
                )
            )
        days.append(
            DayPlan(
                day=index + 1,
                date=current.isoformat(),
                theme=str(raw.get("theme") or fallback.theme)[:80],
                summary=str(raw.get("summary") or fallback.summary)[:280],
                activities=activities or fallback.activities,
            )
        )
    return days




async def generate_ai_itinerary(
    trip: TripRequest,
    settings: Settings
) -> Itinerary:

    daily_budget = round(trip.budget / trip.trip_days, 2)

    prompt = build_itinerary_prompt(
        destination=trip.destination,
        start_date=trip.start_date.isoformat(),
        end_date=trip.end_date.isoformat(),
        travel_style="cultural",
        interests=trip.interests,
        group_size=1,
        pace="moderate",
        budget_per_day=daily_budget,
    )

    system = (
        "You are a practical travel planner for beginners. "
        "Return JSON only with keys days and tips. "
        "days is an array with one object per trip day containing theme, summary, "
        "and activities. Each activity needs time, title, description, estimated_cost. "
        "Keep costs realistic for the daily budget. No markdown."
    )

    async with httpx.AsyncClient(timeout=40) as client:
        response = await client.post(
            OPENAI_URL,
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            },
        )

        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)

    

    tips = [str(tip) for tip in (parsed.get("tips") or [])][:6]
    return Itinerary(
        destination=trip.destination,
        start_date=trip.start_date.isoformat(),
        end_date=trip.end_date.isoformat(),
        budget=trip.budget,
        interests=trip.interests,
        trip_days=trip.trip_days,
        daily_budget=round(trip.budget / trip.trip_days, 2),
        source="ai",
        days=_fallback_days(trip, parsed),
        tips=tips
        or [
            "Confirm opening hours the night before.",
            "Use public transit for most city days.",
        ],
        saved=False,
    )
