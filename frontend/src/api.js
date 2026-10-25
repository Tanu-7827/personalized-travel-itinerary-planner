
const API_BASE = import.meta.env.VITE_API_URL || "";

async function request(path, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 25000);

  let response;

  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(
        "The API took too long to respond. Restart the FastAPI server and try again."
      );
    }

    throw new Error(
      "Could not reach the API. Is the FastAPI server running on port 8000?"
    );
  } finally {
    clearTimeout(timer);
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = data.detail;

    if (typeof detail === "string") {
      throw new Error(detail);
    }

    if (Array.isArray(detail) && detail[0]?.msg) {
      throw new Error(detail[0].msg);
    }

    throw new Error(
      "Something went wrong. Please check your trip details and try again."
    );
  }

  return data;
}

// Check backend and service configuration
export function getHealth() {
  return request("/api/health");
}

// Generate a personalized itinerary
export function createItinerary(payload) {
  return request("/api/itineraries", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// Retrieve previously saved itineraries
export function listItineraries() {
  return request("/api/itineraries");
}

// Get personalized destination recommendations
export function getRecommendations(payload) {
  return request("/api/recommendations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function buildDailyItinerary(payload) {
  return request("/api/daily-itinerary", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}


