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
        if (e?.code === "ERR_CANCELED") return;
        setError("Failed to load topics");
      });
    return () => controller.abort();
  }, []);

  if (error) return <div className="home-error">{error}</div>;
  if (!topics) return <div className="home-status">Loading…</div>;

  return (
    <div className="home-root">
      <section className="home-quick">
        <h2 className="home-h2">Quick Links</h2>
        <div className="home-quick-row">
          <Link to="/questions" className="home-card">
            <div className="home-card-title">Question Bank</div>
            <div className="home-card-sub">Browse and submit answers</div>
          </Link>
        </div>
      </section>

      <section className="home-topics">
        <h2 className="home-h2">Topics</h2>
        <div className="home-topics-row">
          {topics.map((t) => (
            <button
              key={t.id}
              className="home-topic-btn"
              onClick={() => navigate(`/dashboard?topic=${t.id}`)}
            >
              {t.name}
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}
