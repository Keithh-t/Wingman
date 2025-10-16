import { useEffect, useState } from "react";
import { getTopics, type Topic } from "../api/apiClient";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [topics, setTopics] = useState<Topic[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    getTopics().then(setTopics).catch(() => setError("Failed to load topics"));
  }, []);

  if (error) return <div>{error}</div>;
  if (!topics) return <div>Loading…</div>;

  return (
    <div style={{ display: "flex", gap: 12 }}>
      {topics.map((t) => (
        <button key={t.id} onClick={() => navigate(`/dashboard?topic=${t.id}`)}>
          {t.name}
        </button>
      ))}
    </div>
  );
}
