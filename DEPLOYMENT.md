# Deployment

This repository provides the app code and database schema, not provider-specific
deployment manifests. Deploy the backend, frontend, and Supabase project
separately, then configure the frontend to reach the deployed API.

## Before deploying

1. Create a Supabase project if saved itineraries are needed.
2. Apply the existing `supabase/schema.sql` once in that project's SQL Editor.
   Do not create a second itineraries table or duplicate schema.
3. Choose the public frontend origin and backend URL.
4. Configure backend environment variables in the hosting provider's secret
   manager:
   - `SUPABASE_URL` (optional)
   - `SUPABASE_KEY` (optional; keep server-side)
   - `OPENAI_API_KEY` (optional)
   - `FRONTEND_ORIGIN` (set to the deployed frontend origin)

The backend can run without OpenAI and Supabase: sample plans still work, but
trips are not persisted. Never add real credentials to source control, frontend
build variables, logs, or documentation.

## Backend

- Run from `backend/` with the dependencies in `backend/requirements.txt`.
- Start the ASGI app with `uvicorn main:app --host 0.0.0.0 --port <PORT>`,
  replacing `<PORT>` with the port required by the hosting provider.
- Set the provider's start command/port settings accordingly.
- Ensure the host can make outbound HTTPS requests to OpenAI and Supabase when
  those integrations are enabled.
- Check `GET /api/health` after deployment. It reports integration status
  without returning credentials.

The current CORS configuration allows `FRONTEND_ORIGIN` and the local Vite
origin `http://127.0.0.1:5173`. Set `FRONTEND_ORIGIN` to the exact production
origin, including scheme and host.

## Frontend

- Build the existing Vite application from `frontend/` with `npm install` and
  `npm run build`; publish the generated `dist/` directory using a static
  frontend host.
- The local Vite proxy is for development only. In production, set
  `VITE_API_URL` to the backend origin before building, or configure the
  frontend host/reverse proxy to forward `/api` to the backend.
- Configure the static host to serve `index.html` for client-side route
  fallbacks if routes are added later.

`VITE_API_URL` is public browser configuration, not a place for API keys or
passwords.

## Production security checklist

- Keep backend keys in deployment secrets and rotate any key that may have
  been exposed.
- Use HTTPS for the frontend and backend.
- Review the broad read/insert policies in `supabase/schema.sql` before using
  this demo with real users or sensitive data. Restrict access and add
  authentication/authorization as appropriate for the product.
- Review provider logs and access controls; never log request credentials.
- Verify health, itinerary generation, and persistence behavior in the deployed
  environment.
