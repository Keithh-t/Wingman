import { useEffect, useState } from "react";
import { getProgress, type ProgressResponse } from "../api/apiClient";
import "../styles/Progress.css";

export default function Progress() {
  const [data, setData] = useState<ProgressResponse | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await getProgress();
        setData(res);
      } catch (e: any) {
        setErr(e.message || "Failed to load progress");
      }
    })();
  }, []);

  if (err) return <div className="progress-page"><div className="progress-error">{err}</div></div>;
  if (!data) return <div className="progress-page"><div className="progress-loading">Loading…</div></div>;

  // AI formatted
  return (
    <div className="progress-page">
      <div className="progress-header">
        <h2>Your progress</h2>
        <div className="progress-accuracy">Accuracy: {(data.accuracy * 100).toFixed(0)}%</div>
      </div>
      <ul className="progress-list">
        {data.attempts.map((a, i) => (
          <li key={i} className="progress-item">
            <div>
              <div className="progress-row"><span className="muted">Question:</span> {a.question_id}</div>
              <div className="progress-row"><span className="muted">Answer:</span> {a.user_answer}</div>
            </div>
            <span className={`badge ${a.correct ? "ok" : "bad"}`}>
              {a.correct ? "Correct" : "Incorrect"}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
