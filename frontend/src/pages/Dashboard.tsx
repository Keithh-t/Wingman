// src/pages/Dashboard.tsx
import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { getQuestions, getTopics, type Question, type Topic } from "../api/apiClient";
import "../styles/Dashboard.css";

export default function Dashboard() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const topicParam = params.get("topic");
  const topicId = topicParam ? Number(topicParam) : undefined;

  const [qs, setQs] = useState<Question[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  // For showing names instead of Topic #id
  const [topicsMap, setTopicsMap] = useState<Record<number, string>>({});
  const [topicName, setTopicName] = useState<string | null>(null);

  // Load questions
  useEffect(() => {
    const ac = new AbortController();
    setQs(null);
    setError(null);

    // Fetch questions for the selected topic (if any)
    // AI modified to handle topic filter
    getQuestions({ topic_id: topicId }, { signal: ac.signal })
      .then(setQs)
      .catch((e) => {
        const msg = (e as Error)?.message ?? "";
        if (/canceled/i.test(msg)) return; // ignore request cancellations
        setError(msg || "Failed to load questions");
      });

    return () => ac.abort();
  }, [topicId]);

  // Load topics (for names)
  useEffect(() => {
    const ac = new AbortController();

    getTopics()
      .then((ts: Topic[]) => {
        const map = Object.fromEntries(ts.map((t) => [t.id, t.name]));
        setTopicsMap(map);
        setTopicName(topicId ? map[topicId] ?? `Topic #${topicId}` : null);
      })
      .catch(() => {
        setTopicName(topicId ? `Topic #${topicId}` : null);
      });

    return () => ac.abort();
  }, [topicId]);

  if (error) return <div className="error">{error}</div>;
  if (!qs) return <div className="loading">Loading…</div>;

  const showEmptyState = !topicId || qs.length === 0;

  // AI formatted
  return (
    <div className="dashboard">
      <h1 className="page-title">{topicName ?? "Question Bank"}</h1>

      {showEmptyState ? (
        <div className="card empty-card">
          <h2 className="card-title">No topic selected</h2>
          <p className="card-sub">
            Choose a topic on the Home page to see relevant questions.
          </p>
          <button className="btn primary" onClick={() => navigate("/")}>
            Browse Topics
          </button>
        </div>
      ) : (
        <div className="grid">
          {qs.map((q) => {
            const diff = toDifficulty(q.difficulty);
            const subTopic = topicsMap[q.topic_id] ?? `Topic #${q.topic_id}`;
            return (
              <Link key={q.id} to={`/questions/${q.id}`} className="card link-card">
                <div className="card-title-row">
                  <div className="card-title">Question {q.id}</div>
                  <span className={`diff-badge ${diff.cls}`}>{diff.label}</span>
                </div>
                <div className="card-sub clamp-2">{q.question}</div>
                <div className="card-meta">{subTopic}</div>
                <div className="chevron" aria-hidden>›</div>
              </Link>
            );
          })}
        </div>
      )}

      {/* Demo CTA (non-functional) */}
      <div className="cta-wrap">
        <button
          className="btn cta"
          onClick={() => { /* demo no-op */ }}
          aria-label="Take a new diagnostic (demo)"
          title="Take a new diagnostic (demo)"
        >
          Take a New Diagnostic
        </button>
      </div>
    </div>
  );
}

function toDifficulty(d: number): { label: string; cls: string } {
  switch (d) {
    case 1: return { label: "Easy",   cls: "diff-badge--easy" };
    case 2: return { label: "Medium", cls: "diff-badge--medium" };
    case 3: return { label: "Hard",   cls: "diff-badge--hard" };
    default: return { label: `D${d}`, cls: "diff-badge--unknown" };
  }
}
