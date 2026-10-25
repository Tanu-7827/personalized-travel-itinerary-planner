
import jsPDF from "jspdf";

export default function ItineraryView({ itinerary }) {
  if (!itinerary) {
    return (
      <section className="card">
        <h2>Your itinerary will appear here</h2>
        <p className="muted">
          Fill in the trip form and generate a plan. Your daily schedule
          will appear here once it is ready.
        </p>
      </section>
    );
  }

  const days = itinerary.days || [];
  const interests = itinerary.interests || [];
  const tips = itinerary.tips || [];

  const totalDays =
    itinerary.trip_days ?? itinerary.total_days ?? days.length;

  // Convert the itinerary into readable text.
  const createItineraryText = () => {
    const lines = [
      "PERSONALIZED TRAVEL ITINERARY",
      "================================",
      `Destination: ${itinerary.destination || "Not specified"}`,
      `Start Date: ${itinerary.start_date || "Not specified"}`,
      `End Date: ${itinerary.end_date || "Not specified"}`,
      `Total Days: ${totalDays}`,
      `Budget: ${itinerary.budget ?? "Not specified"}`,
      `Interests: ${interests.join(", ") || "Not specified"}`,
      "",
    ];

    days.forEach((day) => {
      lines.push(`DAY ${day.day}: ${day.theme || "Explore"}`);
      lines.push(`Date: ${day.date || "Not specified"}`);

      if (day.summary) {
        lines.push(`Summary: ${day.summary}`);
      }

      lines.push("");

      (day.activities || []).forEach((activity) => {
        lines.push(
          `${activity.time || "Anytime"} - ${
            activity.title || "Local activity"
          }`
        );

        if (activity.description) {
          lines.push(activity.description);
        }

        if (activity.estimated_cost != null) {
          lines.push(`Estimated Cost: $${activity.estimated_cost}`);
        }

        lines.push("");
      });

      lines.push("--------------------------------");
      lines.push("");
    });

    if (tips.length > 0) {
      lines.push("TRAVEL TIPS");

      tips.forEach((tip, index) => {
        lines.push(`${index + 1}. ${tip}`);
      });
    }

    return lines.join("\n");
  };

  // Download the itinerary as a PDF.
  const downloadPDF = () => {
    const pdf = new jsPDF();
    const text = createItineraryText();
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 15;
    const maxWidth = pageWidth - margin * 2;
    const lineHeight = 7;

    const wrappedLines = pdf.splitTextToSize(text, maxWidth);
    let y = margin;

    wrappedLines.forEach((line) => {
      if (y + lineHeight > pageHeight - margin) {
        pdf.addPage();
        y = margin;
      }

      pdf.text(line, margin, y);
      y += lineHeight;
    });

    pdf.save(
      `${(itinerary.destination || "travel-itinerary")
        .replace(/[^a-z0-9]/gi, "-")
        .toLowerCase()}-itinerary.pdf`
    );
  };

  // Download the itinerary as a text file.
  const downloadTXT = () => {
    const text = createItineraryText();
    const blob = new Blob([text], {
      type: "text/plain;charset=utf-8",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "travel-itinerary.txt";
    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
  };

  // Copy the itinerary summary to the clipboard.
  const shareItinerary = async () => {
    const summary = [
      `My travel itinerary: ${itinerary.destination}`,
      `Dates: ${itinerary.start_date || "N/A"} to ${
        itinerary.end_date || "N/A"
      }`,
      `Duration: ${totalDays} days`,
      "",
      ...days.map(
        (day) =>
          `Day ${day.day} (${day.date || "N/A"}): ${
            day.theme || "Explore"
          }\n${(day.activities || [])
            .map(
              (activity) =>
                `- ${activity.time || "Anytime"}: ${
                  activity.title || "Local activity"
                }`
            )
            .join("\n")}`
      ),
    ].join("\n");

    try {
      await navigator.clipboard.writeText(summary);
      alert("Itinerary summary copied! You can now share it.");
    } catch {
      alert(
        "Clipboard access failed. Please use Download TXT to share your itinerary."
      );
    }
  };

  return (
    <section className="card">
      <h2>
        {totalDays} {totalDays === 1 ? "day" : "days"} in{" "}
        {itinerary.destination}
      </h2>

      <div className="meta">
        {itinerary.start_date && itinerary.end_date && (
          <span className="pill">
            {itinerary.start_date} to {itinerary.end_date}
          </span>
        )}

        {itinerary.budget != null && (
          <span className="pill">
            Budget ${Number(itinerary.budget).toFixed(0)}
          </span>
        )}

        {itinerary.daily_budget != null && (
          <span className="pill">
            About ${Number(itinerary.daily_budget).toFixed(0)} / day
          </span>
        )}

        {itinerary.source && (
          <span className="pill">
            {itinerary.source === "ai"
              ? "Generated with AI"
              : "Sample fallback plan"}
          </span>
        )}

        {itinerary.saved != null && (
          <span className="pill">
            {itinerary.saved ? "Saved to Supabase" : "Not saved yet"}
          </span>
        )}
      </div>

      {interests.length > 0 && (
        <p className="muted">Interests: {interests.join(", ")}</p>
      )}

      <div className="export-actions">
        <button type="button" onClick={downloadPDF}>
          Download PDF
        </button>

        <button type="button" onClick={downloadTXT}>
          Download TXT
        </button>

        <button type="button" onClick={shareItinerary}>
          Share Itinerary
        </button>
      </div>

      {days.length > 0 ? (
        <div className="day-grid">
          {days.map((day) => (
            <article
              className="day-card"
              key={`${day.day}-${day.date}`}
            >
              <h3>
                Day {day.day}: {day.theme || "Explore the destination"}
              </h3>

              <p className="muted">{day.date}</p>

              {day.summary && <p>{day.summary}</p>}

              {(day.activities || []).length > 0 ? (
                day.activities.map((activity, index) => (
                  <div
                    className="activity"
                    key={`${day.day}-${activity.time}-${activity.title}-${index}`}
                  >
                    <div className="activity-top">
                      <span>
                        {activity.time || "Anytime"}:{" "}
                        {activity.title || "Local activity"}
                      </span>

                      <span>
                        {activity.estimated_cost != null
                          ? `$${Number(
                              activity.estimated_cost
                            ).toFixed(0)}`
                          : "Cost unavailable"}
                      </span>
                    </div>

                    {activity.description && (
                      <p className="muted">{activity.description}</p>
                    )}
                  </div>
                ))
              ) : (
                <p className="muted">
                  No activities are available for this day.
                </p>
              )}
            </article>
          ))}
        </div>
      ) : (
        <p className="muted">
          No daily activities are available for this itinerary.
        </p>
      )}

      {tips.length > 0 && (
        <div>
          <h3>Travel tips</h3>
          <ul>
            {tips.map((tip, index) => (
              <li key={`${tip}-${index}`}>{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
