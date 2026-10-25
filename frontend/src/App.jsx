import { useEffect, useState } from "react";
import { createItinerary, getHealth, listItineraries } from "./api.js";
import ItineraryView from "./components/ItineraryView.jsx";
import SavedTrips from "./components/SavedTrips.jsx";
import TripForm from "./components/TripForm.jsx";
import DestinationRecommendations from "./components/DestinationRecommendations";
export default function App() {
  const [health, setHealth] = useState(null);
  const [itinerary, setItinerary] = useState(null);
  const [saved, setSaved] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function refreshSaved() {
    try {
      const trips = await listItineraries();
      setSaved(trips);
    } catch {
      setSaved([]);
    }
  }

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() =>
        setHealth({
          status: "offline",
          supabase_configured: false,
          ai_configured: false,
        })
      );
    refreshSaved();
  }, []);

  async function handleGenerate(payload) {
    setLoading(true);
    setError("");
    try {
      const result = await createItinerary(payload);
      setItinerary(result);
      if (result.saved) {
        await refreshSaved();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div className="eyebrow">SkillWallet project</div>
        <h1>Personalized Travel Itinerary Planner</h1>
        <p>
          Enter a destination, dates, budget, and interests. The app builds a
          day-by-day plan with an AI API when configured, or a sample itinerary
          if no key is set.
        </p>
        <div className="status-row">
          <span className="pill">
            API: {health?.status === "ok" ? "connected" : "offline"}
          </span>
          <span className="pill">
            AI: {health?.ai_configured ? "OpenAI ready" : "sample fallback"}
          </span>
          <span className="pill">
            Database: {health?.supabase_configured ? "Supabase ready" : "not configured"}
          </span>
        </div>
      </header>
      <main className="layout">
        <aside className="card">
          <h2>Plan a trip</h2>
          <p className="muted">All fields are validated before the request is sent.</p>
          <TripForm onSubmit={handleGenerate} loading={loading} />
          {error && <div className="error">{error}</div>}
          <SavedTrips
            trips={saved}
            enabled={Boolean(health?.supabase_configured)}
            onSelect={setItinerary}
          />
         
        </aside>
          <DestinationRecommendations />
        
        <ItineraryView itinerary={itinerary} />
      </main>
    </div>
  );
}
