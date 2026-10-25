
from typing import Any


DESTINATIONS = [
    {
        "name": "Kyoto, Japan",
        "interests": ["culture", "history", "food", "nature"],
        "styles": ["cultural", "relaxed", "adventure"],
        "budget_level": "medium",
        "description": "Explore historic temples, traditional streets, gardens, and Japanese cuisine.",
    },
    {
        "name": "Paris, France",
        "interests": ["culture", "history", "food", "art", "photography"],
        "styles": ["cultural", "relaxed"],
        "budget_level": "high",
        "description": "Discover museums, architecture, cafes, art, and famous landmarks.",
    },
    {
        "name": "Bangkok, Thailand",
        "interests": ["food", "culture", "shopping", "history"],
        "styles": ["adventure", "cultural"],
        "budget_level": "low",
        "description": "Enjoy street food, markets, temples, and lively neighborhoods.",
    },
    {
        "name": "Interlaken, Switzerland",
        "interests": ["nature", "adventure", "photography"],
        "styles": ["adventure", "relaxed"],
        "budget_level": "high",
        "description": "Experience alpine scenery, lakes, mountain views, and outdoor activities.",
    },
    {
        "name": "Jaipur, India",
        "interests": ["culture", "history", "food", "photography"],
        "styles": ["cultural", "relaxed"],
        "budget_level": "low",
        "description": "Visit historic forts, colorful markets, palaces, and local food spots.",
    },
]


def recommend_destinations(
    interests: list[str],
    budget: float,
    travel_style: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Return destinations ranked by matching travel preferences."""

    normalized_interests = {
        interest.strip().lower() for interest in interests
    }
    normalized_style = travel_style.strip().lower()

    if budget < 0:
        raise ValueError("Budget cannot be negative.")

    results = []

    for destination in DESTINATIONS:
        matched_interests = normalized_interests.intersection(
            destination["interests"]
        )
        score = len(matched_interests) * 2

        if normalized_style in destination["styles"]:
            score += 3

        if budget <= 500 and destination["budget_level"] == "low":
            score += 2
        elif 500 < budget <= 1500 and destination["budget_level"] == "medium":
            score += 2
        elif budget > 1500 and destination["budget_level"] == "high":
            score += 2

        results.append({
            **destination,
            "score": score,
            "matched_interests": sorted(matched_interests),
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:max(1, min(limit, len(results)))]
