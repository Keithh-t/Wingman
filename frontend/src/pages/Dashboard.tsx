import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getQuestions, type Question } from "../api/apiClient";

export default function Dashboard() {
  const [sp] = useSearchParams();
  const topicId = Number(sp.get("topic")) || undefined;

  const [qs, setQs] = useState<Question[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!topicId) { setQs([]); return; }
    getQuestions({ topic_id: topicId })
      .then(setQs)
      .catch((e) => setError(e.message || "Failed to load questions"));
  }, [topicId]);

  if (error) return <div>{error}</div>;
  if (!qs) return <div>Loading…</div>;
  if (qs.length === 0) return <div>No questions for this topic yet.</div>;

  return (
    <div style={{ display: "grid", gap: 12 }}>
      {qs.map(q => (
        <div key={q.id} style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
          <div style={{ fontWeight: 600 }}>Q{q.id} (diff {q.difficulty})</div>
          <div>{q.question}</div>
        </div>
      ))}
    </div>
  );
}
