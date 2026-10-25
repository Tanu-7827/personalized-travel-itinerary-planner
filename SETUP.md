# Local Setup

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer and npm
- Optional: a Supabase project for saved itineraries
- Optional: an OpenAI API key for AI-generated plans

The app can be run without either external service. In that case, it returns a
sample itinerary and does not save trips.

## Backend

In PowerShell, from the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` if using external services:

```dotenv
SUPABASE_URL=
SUPABASE_KEY=
OPENAI_API_KEY=
FRONTEND_ORIGIN=http://localhost:5173
```

Leave optional values empty to use sample itinerary generation without
persistence. Never commit real keys or passwords. Start the API from the
`backend/` directory:

```powershell
uvicorn main:app --reload --port 8000
```

The health endpoint is at `http://127.0.0.1:8000/api/health`; interactive API
docs are at `http://127.0.0.1:8000/docs`.

## Supabase (optional)

1. Create a Supabase project.
2. Run the existing `supabase/schema.sql` in the Supabase SQL Editor.
3. Set `SUPABASE_URL` and `SUPABASE_KEY` in `backend/.env`, then restart the
   backend.

Use the appropriate server-side key for the deployment model and review the
policies in the schema before using the app with real users.

## Frontend

In a second terminal, from the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The existing Vite configuration proxies `/api`
requests to `http://127.0.0.1:8000`.

For a production build, run `npm run build` inside `frontend/`. Configure the
production host to route `/api` to the backend or set `VITE_API_URL` to the
backend origin before building. This variable is public; do not put secrets in
it.

## Troubleshooting

- If the frontend reports that the API is offline, start the backend and check
  `http://127.0.0.1:8000/api/health`.
- If saved trips are unavailable, confirm the schema was applied and both
  Supabase settings are configured on the backend.
- If the AI integration is not configured, sample itinerary generation is
  expected behavior.
- For browser CORS errors, ensure `FRONTEND_ORIGIN` exactly matches the
  development or deployed frontend origin.
