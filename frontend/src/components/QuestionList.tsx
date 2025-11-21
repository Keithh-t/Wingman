// src/pages/QuestionList.tsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getQuestions, getTopics, type Question, type Topic } from "../api/apiClient";
import "../styles/QuestionList.css";

export default function QuestionsList() {
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [topicsMap, setTopicsMap] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);

    // Load questions
    getQuestions({}, { signal: controller.signal })
      .then((data) => {
        setQuestions(data);
        setErr(null);
      })
      .catch((e: any) => {
        if (e?.code === "ERR_CANCELED") return;
        setErr(e?.message || "Failed to load questions");
      })
      .finally(() => setLoading(false));

    // Load topics just once (for names)
    getTopics()
      .then((ts: Topic[]) => {
        const map = Object.fromEntries(ts.map((t) => [t.id, t.name]));
        setTopicsMap(map);
      })
      .catch(() => { /* non-critical; leave map empty */ });

    return () => controller.abort();
  }, []);

  // AI formatted
  return (
    <div className="ql-root">
      <h1 className="ql-title">Question Bank</h1>

      {loading && <p className="ql-status">Loading questions…</p>}
      {!loading && err && <p className="ql-error">Error: {err}</p>}

      {!loading && !err && questions && questions.length === 0 && (
        <p className="ql-status">No questions available yet.</p>
      )}

      {!loading && !err && questions && questions.length > 0 && (
        <ul className="ql-list">
          {questions.map((q) => {
            const { label, cls } = toDifficulty(q.difficulty);
            const topicName = topicsMap[q.topic_id] ?? `Topic #${q.topic_id}`;
            return (
              <li key={q.id} className="ql-item">
                <div className="ql-item-main">
                  <Link to={`/questions/${q.id}`} className="ql-link">
                    {truncate(q.question, 140)}
                  </Link>
                  <div className="ql-subtext">{topicName}</div>
                </div>
                <span className={`ql-badge ${cls}`}>{label}</span>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

function truncate(s: string, n: number) {
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}

function toDifficulty(d: number): { label: string; cls: string } {
  switch (d) {
    case 1: return { label: "Easy",   cls: "ql-badge--easy" };
    case 2: return { label: "Medium", cls: "ql-badge--medium" };
    case 3: return { label: "Hard",   cls: "ql-badge--hard" };
    default: return { label: `D${d}`, cls: "ql-badge--unknown" };
  }
}
