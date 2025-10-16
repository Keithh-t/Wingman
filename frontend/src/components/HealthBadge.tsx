import { useEffect, useState } from "react";
import { getHealth } from "../api/apiClient";

export default function HealthBadge() {
  const [status, setStatus] = useState<"…" | "ok" | "error">("…");
  useEffect(() => {
    getHealth().then(() => setStatus("ok")).catch(() => setStatus("error"));
  }, []);
  return <span style={{ marginLeft: 8, border: "1px solid #ccc", padding: "2px 8px", borderRadius: 8 }}>
    health: {status}
  </span>;
}
