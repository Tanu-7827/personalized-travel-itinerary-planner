
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from httpx import HTTPError
from pydantic import BaseModel, Field

from ai_itinerary import generate_ai_itinerary
from app.services.itinerary_builder import build_daily_itinerary
from app.services.recommendation import recommend_destinations
from config import get_settings
from db import (
    delete_itinerary,
    get_itinerary,
    list_itineraries,
    save_itinerary,
    update_itinerary,
)
from models import HealthResponse, Itinerary, TripRequest
from sample_itinerary import build_sample_itinerary

logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title="Personalized Travel Itinerary Planner",
    description="API for personalized travel planning and itinerary management.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(
        {
            settings.frontend_origin,
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        }
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    interests: list[str] = Field(default_factory=list)
    budget: float = Field(gt=0)
    travel_style: str = "cultural"
    limit: int = Field(default=3, ge=1, le=5)


class DailyItineraryRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    interests: list[str] = Field(
        default_factory=lambda: ["sightseeing"]
    )
    travel_pace: str = "balanced"


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        supabase_configured=settings.supabase_configured,
        ai_configured=settings.openai_configured,
    )


@app.post("/api/itineraries", response_model=Itinerary)
async def create_itinerary(trip: TripRequest) -> Itinerary:
    if settings.openai_configured:
        try:
            itinerary = await generate_ai_itinerary(trip, settings)
        except (HTTPError, ValueError, KeyError, TypeError) as exc:
            logger.exception("AI itinerary generation failed: %s", exc)
            itinerary = build_sample_itinerary(trip)
    else:
        logger.warning("OpenAI is not configured. Using sample itinerary.")
        itinerary = build_sample_itinerary(trip)

    if settings.supabase_configured:
        try:
            itinerary = save_itinerary(settings, itinerary)
        except Exception as exc:
            logger.exception("Could not save itinerary.")
            raise HTTPException(
                status_code=503,
                detail="The itinerary was generated, but saving to Supabase failed.",
            ) from exc

    return itinerary


@app.get("/api/itineraries", response_model=list[Itinerary])
def get_saved_itineraries() -> list[Itinerary]:
    if not settings.supabase_configured:
        return []

    try:
        return list_itineraries(settings)
    except Exception as exc:
        logger.exception("Could not retrieve itineraries.")
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve saved itineraries.",
        ) from exc


@app.get("/api/itineraries/{itinerary_id}", response_model=Itinerary)
def get_saved_itinerary(itinerary_id: str) -> Itinerary:
    if not settings.supabase_configured:
        raise HTTPException(
            status_code=503,
            detail="Supabase is not configured.",
        )

    try:
        itinerary = get_itinerary(settings, itinerary_id)
    except Exception as exc:
        logger.exception("Could not retrieve itinerary.")
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve itinerary.",
        ) from exc

    if itinerary is None:
        raise HTTPException(
            status_code=404,
            detail="Itinerary not found.",
        )

    return itinerary


@app.put("/api/itineraries/{itinerary_id}", response_model=Itinerary)
def update_saved_itinerary(
    itinerary_id: str,
    itinerary: Itinerary,
) -> Itinerary:
    if not settings.supabase_configured:
        raise HTTPException(
            status_code=503,
            detail="Supabase is not configured.",
        )

    try:
        updated = update_itinerary(settings, itinerary_id, itinerary)
    except Exception as exc:
        logger.exception("Could not update itinerary.")
        raise HTTPException(
            status_code=503,
            detail="Could not update itinerary.",
        ) from exc

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Itinerary not found.",
        )

    return updated


@app.delete("/api/itineraries/{itinerary_id}")
def remove_saved_itinerary(itinerary_id: str) -> dict:
    if not settings.supabase_configured:
        raise HTTPException(
            status_code=503,
            detail="Supabase is not configured.",
        )

    try:
        deleted = delete_itinerary(settings, itinerary_id)
    except Exception as exc:
        logger.exception("Could not delete itinerary.")
        raise HTTPException(
            status_code=503,
            detail="Could not delete itinerary.",
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Itinerary not found.",
        )

    return {
        "message": "Itinerary deleted successfully.",
        "id": itinerary_id,
    }


@app.post("/api/recommendations")
def get_recommendations(
    request: RecommendationRequest,
) -> dict:
    try:
        recommendations = recommend_destinations(
            interests=request.interests,
            budget=request.budget,
            travel_style=request.travel_style,
            limit=request.limit,
        )
        return {"recommendations": recommendations}
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/api/daily-itinerary")
def create_daily_itinerary(
    request: DailyItineraryRequest,
) -> dict:
    try:
        days = build_daily_itinerary(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            interests=request.interests,
            travel_pace=request.travel_pace,
        )
        return {
            "destination": request.destination,
            "days": days,
            "total_days": len(days),
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc