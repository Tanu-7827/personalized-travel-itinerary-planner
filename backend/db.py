
import httpx

from config import Settings
from models import Itinerary

TABLE = "itineraries"


def _headers(settings: Settings) -> dict[str, str]:
    return {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _rest_url(settings: Settings, path: str = "") -> str:
    return f"{settings.supabase_url.rstrip('/')}/rest/v1/{TABLE}{path}"


def itinerary_to_row(itinerary: Itinerary) -> dict:
    return {
        "destination": itinerary.destination,
        "start_date": itinerary.start_date,
        "end_date": itinerary.end_date,
        "budget": itinerary.budget,
        "interests": itinerary.interests,
        "trip_days": itinerary.trip_days,
        "daily_budget": itinerary.daily_budget,
        "source": itinerary.source,
        "days": [day.model_dump() for day in itinerary.days],
        "tips": itinerary.tips,
    }


def row_to_itinerary(row: dict) -> Itinerary:
    return Itinerary(
        id=str(row.get("id") or ""),
        destination=row["destination"],
        start_date=str(row["start_date"]),
        end_date=str(row["end_date"]),
        budget=float(row["budget"]),
        interests=list(row.get("interests") or []),
        trip_days=int(row.get("trip_days") or len(row.get("days") or [])),
        daily_budget=float(row.get("daily_budget") or 0),
        source=row.get("source") or "sample",
        days=row.get("days") or [],
        tips=list(row.get("tips") or []),
        saved=True,
    )


def save_itinerary(settings: Settings, itinerary: Itinerary) -> Itinerary:
    response = httpx.post(
        _rest_url(settings),
        headers=_headers(settings),
        json=itinerary_to_row(itinerary),
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    row = data[0] if isinstance(data, list) else data

    if not row:
        raise RuntimeError("Supabase did not return the saved itinerary.")

    return row_to_itinerary(row)


def list_itineraries(
    settings: Settings,
    limit: int = 12,
) -> list[Itinerary]:
    response = httpx.get(
        _rest_url(settings),
        headers=_headers(settings),
        params={
            "select": "*",
            "order": "created_at.desc",
            "limit": str(limit),
        },
        timeout=20,
    )
    response.raise_for_status()

    return [
        row_to_itinerary(row)
        for row in (response.json() or [])
    ]


def get_itinerary(
    settings: Settings,
    itinerary_id: str,
) -> Itinerary | None:
    response = httpx.get(
        _rest_url(settings),
        headers=_headers(settings),
        params={
            "select": "*",
            "id": f"eq.{itinerary_id}",
            "limit": "1",
        },
        timeout=20,
    )
    response.raise_for_status()

    rows = response.json()

    if not rows:
        return None

    return row_to_itinerary(rows[0])


def update_itinerary(
    settings: Settings,
    itinerary_id: str,
    itinerary: Itinerary,
) -> Itinerary | None:
    response = httpx.patch(
        _rest_url(settings),
        headers=_headers(settings),
        params={"id": f"eq.{itinerary_id}"},
        json=itinerary_to_row(itinerary),
        timeout=20,
    )
    response.raise_for_status()

    rows = response.json()

    if not rows:
        return None

    return row_to_itinerary(rows[0])


def delete_itinerary(
    settings: Settings,
    itinerary_id: str,
) -> bool:
    response = httpx.delete(
        _rest_url(settings),
        headers=_headers(settings),
        params={"id": f"eq.{itinerary_id}"},
        timeout=20,
    )
    response.raise_for_status()

    # Supabase returns deleted rows because Prefer is set
    # to return=representation.
    return bool(response.json())

