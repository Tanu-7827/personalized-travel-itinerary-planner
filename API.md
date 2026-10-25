# API Reference

The FastAPI backend exposes a small JSON API for health checks and personalized
itineraries. During local development, the Vite server forwards `/api` requests
to `http://127.0.0.1:8000`.

Interactive documentation is available at `http://127.0.0.1:8000/docs` while
the backend is running.

## Base path

All application endpoints use the `/api` prefix.

## `GET /api/health`

Returns the API status and whether optional integrations have credentials
configured. The response does not expose credentials.

Example response:

```json
{
  "status": "ok",
  "supabase_configured": false,
  "ai_configured": false
}
```

## `POST /api/itineraries`

Validates trip details and creates a day-by-day plan. If `OPENAI_API_KEY` is
configured, the backend tries to use OpenAI; otherwise, or if that request
fails, it builds a sample itinerary. If Supabase is configured, the result is
also saved and returned with `saved: true`.

Request:

```json
{
  "destination": "Kyoto",
  "start_date": "2026-11-10",
  "end_date": "2026-11-12",
  "budget": 1200,
  "interests": ["food", "culture"]
}
```

Validation:

- `destination`: 2-80 characters; letters, spaces, hyphens, and apostrophes.
- `start_date` and `end_date`: ISO dates; end date must not precede start date.
- Trip length: at most 14 calendar days, including both endpoints.
- `budget`: number from 1 through 1,000,000.
- `interests`: 1-6 distinct values from `food`, `culture`, `nature`,
  `adventure`, `relaxation`, `nightlife`, `shopping`, and `history`.

Response fields include `id` (when saved), destination and dates, budget,
interests, `trip_days`, `daily_budget`, `source` (`ai` or `sample`), `days`,
`tips`, and `saved`. Each day contains its day number, date, theme, summary, and
activities. Each activity contains a time, title, description, and estimated
cost.

Typical errors include `422` for invalid request data and `503` if saving to or
loading from configured Supabase fails.

## `GET /api/itineraries`

Returns the most recent saved itineraries (up to 12). When Supabase is not
configured, the endpoint returns an empty array.

## Related files

- Request and response validation: `backend/models.py`
- Endpoint handlers: `backend/main.py`
- Supabase persistence: `backend/db.py`
- API client used by the React app: `frontend/src/api.js`
