import { useEffect, useState } from "react";
import { getTopics, type Topic } from "../api/apiClient";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Home.css";

export default function Home() {
  const [topics, setTopics] = useState<Topic[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const controller = new AbortController();
    getTopics()
      .then(setTopics)
      .catch((e: any) => {
        if (e?.code === "ERR_CANCELED" || /canceled/i.test(e?.message ?? "")) return;
        setError("Failed to load topics");
      });
    return () => controller.abort();
  }, []);

  if (error) return <div className="home-error">{error}</div>;
  if (!topics) return <div className="home-status">Loading…</div>;

  // AI formatted
  return (
    <div className="home-root">
      {/* Hero */}
      <section className="home-hero">
        <h1>Wingman</h1>
        <p>Your co-pilot for mastering Mechanical & Aerospace interview questions.</p>
      </section>

      {/* Get Started / Quick Links */}
      <section className="quick-links">
        <h2>Get Started</h2>
        <div className="ql-grid">
          <Link to="/questions" className="ql-card">
            <h3>Question Bank</h3>
            <p>Browse and practice technical questions.</p>
          </Link>
          <Link to="/progress" className="ql-card">
            <h3>Progress</h3>
            <p>Check accuracy and recent attempts.</p>
          </Link>
        </div>
      </section>

      {/* Topics */}
      <section className="home-topics">
        <h2 className="topics-title">Topics</h2>
        <div className="topics">
          {topics.map((t) => (
            <button
              key={t.id}
              className="topic-button"
              onClick={() => navigate(`/dashboard?topic=${t.id}`)}
            >
              {t.name}
            </button>
          ))}
        </div>
      </section>

      {/* CTA */}
      <div className="home-cta">
        <Link to="/dashboard" className="btn cta">Start Practicing</Link>
      </div>
    </div>
  );
}
