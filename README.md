# Personalized Travel Itinerary Planner

A beginner-friendly SkillWallet project. Students enter a destination, trip dates, budget, and interests. A FastAPI backend builds a day-by-day itinerary, optionally with OpenAI, and can save trips in Supabase.

If `OPENAI_API_KEY` is missing, the backend still returns a complete sample itinerary so the app is easy to demo.

## Folder structure

```text
personalized-travel-itinerary-planner/
├── README.md
├── .gitignore
├── backend/
│   ├── main.py                 # FastAPI routes
│   ├── config.py               # Reads env vars, never hardcodes secrets
│   ├── models.py               # Request/response validation
│   ├── sample_itinerary.py     # Fallback plan
│   ├── ai_itinerary.py         # Optional OpenAI call
│   ├── db.py                   # Optional Supabase save/list
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── .env.example
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/
└── supabase/
    └── schema.sql              # Table + beginner demo policies
```

## What you need

- Node.js 18+
- Python 3.10+
- A free [Supabase](https://supabase.com) project if you want saved trips
- An [OpenAI](https://platform.openai.com) API key if you want AI-generated plans

You can run the app without Supabase or OpenAI. In that case the sample itinerary is shown and nothing is saved.

## 1. Create a virtual environment and start the backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Open `backend/.env` and fill in values if you have them:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
OPENAI_API_KEY=
FRONTEND_ORIGIN=http://localhost:5173
```

Start the API:

```bash
uvicorn main:app --port 8000
```

Optional auto-reload while you edit Python files:

```bash
uvicorn main:app --reload --port 8000 --reload-exclude .venv
```

On Windows, especially inside OneDrive, `--reload` can restart too often because it watches `.venv`. If generate requests hang, run without `--reload`.

Open http://127.0.0.1:8000/docs to see the interactive API.

## 2. Set up Supabase (optional, for saving trips)

1. Create a project at https://supabase.com.
2. Open **SQL Editor**, paste `supabase/schema.sql`, and run it.
3. Open **Project Settings -> API**.
4. Copy **Project URL** into `SUPABASE_URL`.
5. Copy the **anon public** key into `SUPABASE_KEY`.
6. Restart the FastAPI server so it picks up the new `.env` values.

The SQL file creates an `itineraries` table and simple read/insert policies so a beginner demo can save and list trips.

## 3. Start the React frontend

```bash
cd frontend
npm install
copy .env.example .env   # optional; the Vite proxy works without this
npm run dev
```

Open http://localhost:5173.

The Vite config proxies `/api` to FastAPI on port 8000, so you do not need `VITE_API_URL` during local development.

## How the app works

1. The React form validates destination, dates, budget, and interests.
2. It posts JSON to `POST /api/itineraries`.
3. FastAPI validates the same fields again with Pydantic.
4. If `OPENAI_API_KEY` is set, the backend asks OpenAI for a JSON itinerary.
5. If the key is missing or the AI call fails, `sample_itinerary.py` builds a readable fallback.
6. If Supabase is configured, the backend saves the itinerary with the Supabase REST API (`/rest/v1/itineraries`).
7. `GET /api/itineraries` lists recently saved trips.

## API summary

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Shows whether AI and Supabase are configured |
| POST | `/api/itineraries` | Generate (and optionally save) a plan |
| GET | `/api/itineraries` | List saved plans |

Example request body:

```json
{
  "destination": "Kyoto",
  "start_date": "2026-11-10",
  "end_date": "2026-11-13",
  "budget": 1200,
  "interests": ["food", "culture"]
}
```

## Validation rules

- Destination: 2-80 characters, letters/spaces/hyphens/apostrophes
- Dates: end date on or after start date, maximum 14 days
- Budget: number from 1 to 1,000,000
- Interests: at least one from food, culture, nature, adventure, relaxation, nightlife, shopping, history

## Security notes

- Secrets live only in `.env` files, which are ignored by git.
- Copy `.env.example` files; never put real keys in source code.
- The backend is the only place that talks to OpenAI and Supabase.

## Troubleshooting

- **Frontend says the API is offline:** start FastAPI first, then refresh http://localhost:5173.
- **Supabase save fails:** confirm `schema.sql` was run and the URL/key in `backend/.env` are correct.
- **AI is not used:** that is expected when `OPENAI_API_KEY` is empty. The sample itinerary is the assignment fallback.
- **CORS errors:** keep `FRONTEND_ORIGIN=http://localhost:5173` and use the Vite dev server.

## Assignment talking points

- Frontend and backend are separated, which is a common full-stack pattern.
- Validation happens on both sides so bad data is rejected early.
- AI is optional, so the demo still works without paid keys.
- Supabase is a hosted Postgres database with a simple table for itineraries.
