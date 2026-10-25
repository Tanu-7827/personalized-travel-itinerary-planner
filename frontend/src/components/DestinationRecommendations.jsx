
import { useState } from "react";
import { getRecommendations } from "../api";

export default function DestinationRecommendations() {
  const [interests, setInterests] = useState(["culture", "history"]);
  const [budget, setBudget] = useState("400");
  const [travelStyle, setTravelStyle] = useState("cultural");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const availableInterests = [
    "food",
    "culture",
    "nature",
    "adventure",
    "shopping",
    "history",
    "photography",
    "art",
  ];

  function toggleInterest(value) {
    setInterests((current) =>
      current.includes(value)
        ? current.filter((item) => item !== value)
        : [...current, value]
    );
  }

  async function handleRecommend(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResults([]);

    try {
      const data = await getRecommendations({
        interests,
        budget: Number(budget),
        travel_style: travelStyle,
        limit: 3,
      });
      setResults(data.recommendations || []);
    } catch (err) {
      setError(err.message || "Could not load recommendations.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="form">
      <h2>Discover Destinations</h2>
      <p className="muted">
        Find destinations that match your interests, budget, and travel style.
      </p>

      <form onSubmit={handleRecommend}>
        <strong>Choose your interests</strong>
        <div className="interests">
          {availableInterests.map((interest) => (
            <label className="chip" key={interest}>
              <input
                type="checkbox"
                checked={interests.includes(interest)}
                onChange={() => toggleInterest(interest)}
              />
              {interest}
            </label>
          ))}
        </div>

        <label>
          Budget (USD)
          <input
            type="number"
            min="1"
            step="0.01"
            required
            value={budget}
            onChange={(event) => setBudget(event.target.value)}
          />
        </label>

        <label>
          Travel style
          <select
            value={travelStyle}
            onChange={(event) => setTravelStyle(event.target.value)}
          >
            <option value="cultural">Cultural</option>
            <option value="adventure">Adventure</option>
            <option value="relaxed">Relaxed</option>
          </select>
        </label>

        <button className="primary" disabled={loading} type="submit">
          {loading ? "Finding destinations..." : "Get Recommendations"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {results.length > 0 && (
        <div>
          <h3>Recommended destinations</h3>
          {results.map((item) => (
            <article
              key={item.name}
              style={{
                border: "1px solid #ddd",
                borderRadius: "10px",
                padding: "16px",
                marginTop: "12px",
              }}
            >
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <p>
                <strong>Matched interests:</strong>{" "}
                {item.matched_interests?.join(", ") || "No direct matches"}
              </p>
              <p>
                <strong>Match score:</strong> {item.score}
              </p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
