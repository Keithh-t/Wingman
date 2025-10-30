import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getQuestions, type Question } from "../api/apiClient";
import "../styles/QuestionList.css";

export default function QuestionsList() {
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);

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

    return () => controller.abort();
  }, []);

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
          {questions.map((q) => (
            <li key={q.id} className="ql-item">
              <div className="ql-item-main">
                <Link to={`/questions/${q.id}`} className="ql-link">
                  {truncate(q.question, 140)}
                </Link>
                <div className="ql-subtext">Topic #{q.topic_id}</div>
              </div>
              <span className="ql-badge">D{q.difficulty}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// ai suggested
function truncate(s: string, n: number) {
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}
