
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


MAX_TRIP_DAYS = 14
MIN_BUDGET = 1
MAX_BUDGET = 1_000_000

ALLOWED_INTERESTS = {
    "food",
    "culture",
    "nature",
    "adventure",
    "relaxation",
    "nightlife",
    "shopping",
    "history",
}


class TripRequest(BaseModel):
    destination: str = Field(..., min_length=2, max_length=80)
    start_date: date
    end_date: date
    budget: float = Field(..., ge=MIN_BUDGET, le=MAX_BUDGET)
    interests: list[str] = Field(..., min_length=1, max_length=6)

    @field_validator("destination")
    @classmethod
    def clean_destination(cls, value: str) -> str:
        cleaned = " ".join(value.strip().split())
        if len(cleaned) < 2:
            raise ValueError("Destination must be at least 2 characters.")
        if not all(ch.isalpha() or ch in " -'" for ch in cleaned):
            raise ValueError(
                "Destination can only contain letters, spaces, hyphens, and apostrophes."
            )
        return cleaned.title()

    @field_validator("interests")
    @classmethod
    def normalize_interests(cls, values: list[str]) -> list[str]:
        cleaned = []
        for item in values:
            key = item.strip().lower()
            if key not in ALLOWED_INTERESTS:
                raise ValueError(
                    f"Unsupported interest '{item}'. Choose from: "
                    f"{', '.join(sorted(ALLOWED_INTERESTS))}."
                )
            if key not in cleaned:
                cleaned.append(key)
        if not cleaned:
            raise ValueError("Select at least one interest.")
        return cleaned

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be on or after the start date.")
        trip_days = (self.end_date - self.start_date).days + 1
        if trip_days > MAX_TRIP_DAYS:
            raise ValueError(f"Trips can be at most {MAX_TRIP_DAYS} days long.")
        return self

    @property
    def trip_days(self) -> int:
        return (self.end_date - self.start_date).days + 1


class Activity(BaseModel):
    time: str
    title: str
    description: str
    estimated_cost: float = 0


class DayPlan(BaseModel):
    day: int
    date: str
    theme: str
    summary: str
    activities: list[Activity]


class Itinerary(BaseModel):
    id: str | None = None
    destination: str
    start_date: str
    end_date: str
    budget: float
    interests: list[str]
    trip_days: int
    daily_budget: float
    source: Literal["ai", "sample"]
    days: list[DayPlan]
    tips: list[str] = Field(default_factory=list)
    saved: bool = False


class HealthResponse(BaseModel):
    status: str
    supabase_configured: bool
    ai_configured: bool


