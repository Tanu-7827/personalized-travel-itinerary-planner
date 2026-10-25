export default function SavedTrips({ trips, onSelect, enabled }) {
  return (
    <div>
      <h3>Saved trips</h3>
      {!enabled && (
        <p className="muted">
          Add Supabase keys to save itineraries. You can still generate plans without them.
        </p>
      )}
      {enabled && trips.length === 0 && (
        <p className="muted">No saved itineraries yet. Generate one to store it.</p>
      )}
      <div className="saved-list">
        {trips.map((trip) => (
          <button
            key={trip.id}
            className="ghost"
            type="button"
            onClick={() => onSelect(trip)}
          >
            {trip.destination} · {trip.start_date}
          </button>
        ))}
      </div>
    </div>
  );
}
