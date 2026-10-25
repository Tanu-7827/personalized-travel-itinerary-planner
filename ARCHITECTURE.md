# Architecture

## Overview

The project is a small full-stack travel planner:

```text
React + Vite browser app
        |
        | JSON requests to /api
        v
FastAPI backend
   |                 |
   | optional AI     | optional persistence
   v                 v
OpenAI API         Supabase REST API
```

The React app collects a destination, dates, budget, and interests. The FastAPI
backend validates the request, generates a plan using OpenAI when configured
(with a local sample-plan fallback), and optionally saves and lists plans in
Supabase.

## Existing application modules

- `frontend/src/App.jsx` coordinates form submission, health status, and saved
  trips.
- `frontend/src/components/` contains the trip form, itinerary display, and
  saved-trip components.
- `frontend/src/api.js` calls the backend API.
- `backend/main.py` defines the health and itinerary endpoints and CORS policy.
- `backend/models.py` validates trip requests and defines response models.
- `backend/config.py` loads environment-based settings.
- `backend/ai_itinerary.py` calls the OpenAI chat completions API and validates
  the generated itinerary data.
- `backend/sample_itinerary.py` builds the offline/demo itinerary.
- `backend/db.py` communicates with the Supabase REST API.
- `supabase/schema.sql` defines the existing `itineraries` table and its
  policies; use this schema rather than creating a duplicate.

The `backend/app/` package folders and `frontend/src/pages/` and
`frontend/src/services/` directories are scaffold locations. The working
backend modules currently remain at the `backend/` root, and the frontend API
client currently remains at `frontend/src/api.js`. The scaffold does not move
or replace those modules.

## Runtime flow

1. The browser submits `POST /api/itineraries`.
2. FastAPI validates the payload with Pydantic.
3. The backend attempts AI generation if an OpenAI key is configured. If AI is
   unavailable or the call fails, it returns the sample itinerary.
4. When Supabase settings are present, the backend saves the result and
   returns the saved row.
5. The browser can load saved results with `GET /api/itineraries`.

For local development, Vite proxies `/api` to the backend on port 8000. This
proxy is a development-server setting; production hosting must route `/api`
to the backend or configure the frontend API base URL.

## Configuration and trust boundaries

Backend credentials belong in `backend/.env` or the hosting provider's secret
configuration. Only the backend calls OpenAI and Supabase. Never place these
credentials in frontend source or a `VITE_` variable. The health endpoint
reports only whether integrations are configured, not their secret values.
