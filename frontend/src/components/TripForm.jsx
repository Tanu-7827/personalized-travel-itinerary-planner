
import { useMemo, useState } from "react";

const INTERESTS = [
  "food",
  "culture",
  "nature",
  "adventure",
  "relaxation",
  "nightlife",
  "shopping",
  "history",
];

function todayIso() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function addDays(isoDate, days) {
  const date = new Date(`${isoDate}T12:00:00`);
  date.setDate(date.getDate() + days);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export default function TripForm({ onSubmit, loading }) {
  const minStart = todayIso();

  const [form, setForm] = useState({
    destination: "Kyoto",
    start_date: addDays(minStart, 14),
    end_date: addDays(minStart, 17),
    budget: "1200",
    travelers: "1",
    interests: ["food", "culture"],
    dietary_needs: "none",
    travel_pace: "balanced",
    travel_vibe: "cultural",
  });

  const [errors, setErrors] = useState([]);

  const tripDays = useMemo(() => {
    if (!form.start_date || !form.end_date) return 0;

    const start = new Date(`${form.start_date}T00:00:00`);
    const end = new Date(`${form.end_date}T00:00:00`);

    return Math.floor((end - start) / 86400000) + 1;
  }, [form.start_date, form.end_date]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function toggleInterest(interest) {
    setForm((current) => {
      const interests = current.interests.includes(interest)
        ? current.interests.filter((item) => item !== interest)
        : [...current.interests, interest];

      return { ...current, interests };
    });
  }

  function validate() {
    const next = [];
    const budget = Number(form.budget);
    const travelers = Number(form.travelers);

    if (form.destination.trim().length < 2) {
      next.push("Enter a destination with at least 2 letters.");
    }

    if (!form.start_date || !form.end_date) {
      next.push("Choose both a start date and an end date.");
    } else if (form.start_date < minStart) {
      next.push("Start date cannot be in the past.");
    } else if (form.end_date < form.start_date) {
      next.push("End date must be on or after the start date.");
    } else if (tripDays > 14) {
      next.push("Keep the trip to 14 days or fewer.");
    }

    if (!Number.isFinite(budget) || budget < 1) {
      next.push("Budget must be greater than 0.");
    }

    if (!Number.isInteger(travelers) || travelers < 1 || travelers > 50) {
      next.push("Travellers must be between 1 and 50.");
    }

    if (form.interests.length === 0) {
      next.push("Select at least one interest.");
    }

    setErrors(next);
    return next.length === 0;
  }

  function handleSubmit(event) {
    event.preventDefault();

    if (!validate()) return;

    onSubmit({
      destination: form.destination.trim(),
      start_date: form.start_date,
      end_date: form.end_date,
      budget: Number(form.budget),
      travelers: Number(form.travelers),
      interests: form.interests,
      dietary_needs: form.dietary_needs,
      travel_pace: form.travel_pace,
      travel_vibe: form.travel_vibe,
    });
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <label>
        Destination
        <input
          required
          value={form.destination}
          onChange={(event) => update("destination", event.target.value)}
          placeholder="City or region"
        />
      </label>

      <label>
        Start date
        <input
          required
          type="date"
          min={minStart}
          value={form.start_date}
          onChange={(event) => update("start_date", event.target.value)}
        />
      </label>

      <label>
        End date
        <input
          required
          type="date"
          min={form.start_date || minStart}
          value={form.end_date}
          onChange={(event) => update("end_date", event.target.value)}
        />
      </label>

      <label>
        Total budget (USD)
        <input
          required
          type="number"
          min="1"
          step="0.01"
          value={form.budget}
          onChange={(event) => update("budget", event.target.value)}
        />
      </label>

      <label>
        Number of travellers
        <input
          required
          type="number"
          min="1"
          max="50"
          step="1"
          value={form.travelers}
          onChange={(event) => update("travelers", event.target.value)}
        />
      </label>

      <div>
        <strong>Interests</strong>
        <div className="interests">
          {INTERESTS.map((interest) => (
            <label className="chip" key={interest}>
              <input
                type="checkbox"
                checked={form.interests.includes(interest)}
                onChange={() => toggleInterest(interest)}
              />
              {interest}
            </label>
          ))}
        </div>
      </div>

      <label>
        Dietary requirements
        <select
          value={form.dietary_needs}
          onChange={(event) => update("dietary_needs", event.target.value)}
        >
          <option value="none">No special requirements</option>
          <option value="vegetarian">Vegetarian</option>
          <option value="vegan">Vegan</option>
          <option value="halal">Halal</option>
          <option value="jain">Jain</option>
          <option value="gluten_free">Gluten-free</option>
          <option value="other">Other</option>
        </select>
      </label>

      <label>
        Travel vibe
        <select
          value={form.travel_vibe}
          onChange={(event) => update("travel_vibe", event.target.value)}
        >
          <option value="relaxed">Relaxed</option>
          <option value="adventure">Adventure</option>
          <option value="cultural">Cultural</option>
          <option value="luxury">Luxury</option>
          <option value="budget">Budget-friendly</option>
        </select>
      </label>

      <label>
        Travel pace
        <select
          value={form.travel_pace}
          onChange={(event) => update("travel_pace", event.target.value)}
        >
          <option value="relaxed">Relaxed — fewer activities</option>
          <option value="balanced">Balanced — moderate activities</option>
          <option value="packed">Packed — more activities</option>
        </select>
      </label>

      <p className="muted">
        {tripDays > 0 ? `${tripDays} day trip` : "Choose valid dates"}
      </p>

      {errors.map((error) => (
        <div className="error" key={error}>
          {error}
        </div>
      ))}

      <button className="primary" type="submit" disabled={loading}>
        {loading ? "Building itinerary..." : "Generate itinerary"}
      </button>
    </form>
  );
}



