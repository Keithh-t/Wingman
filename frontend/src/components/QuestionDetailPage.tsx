import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getQuestionById, postAttempt, 
type QuestionDetail, type AttemptResult } from "../api/apiClient";
import "../styles/QuestionDetailPage.css";

// mostly ai suggested
export default function QuestionDetailPage() {
  const { id } = useParams();
  const qid = useMemo(() => {
    const n = Number(id);
    return Number.isFinite(n) && n > 0 ? n : null;
  }, [id]);

  const [question, setQuestion] = useState<QuestionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  const [answer, setAnswer] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<AttemptResult | null>(null);

  useEffect(() => {
    if (!qid) {
      setErr("Invalid question id");
      setLoading(false);
      return;
    }
    const controller = new AbortController();
    setLoading(true);
    setResult(null);

    getQuestionById(qid, { signal: controller.signal })
      .then((data) => {
        setQuestion(data);
        setErr(null);
      })
      .catch((e: any) => {
        if (e?.code === "ERR_CANCELED") return;
        setErr(e?.message ?? "Failed to load question");
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [qid]);

  const submitControllerRef = useRef<AbortController | null>(null);
  useEffect(() => {
    return () => submitControllerRef.current?.abort();
  }, []);

  const canSubmit = !!qid && answer.trim().length > 0 && !submitting;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!qid || !canSubmit) return;

    submitControllerRef.current?.abort();
    const controller = new AbortController();
    submitControllerRef.current = controller;

    setSubmitting(true);
    try {
      const r = await postAttempt(
        { question_id: qid, user_answer: answer },
        { signal: controller.signal }
      );
      setResult(r);
    } catch (e: any) {
      if (e?.code !== "ERR_CANCELED") {
        setResult({ correct: false, feedback: e?.message ?? "Submission failed" });
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="qd-root">
      <div className="qd-header">
        <h1 className="qd-title">Question</h1>
        <Link to="/questions" className="qd-back">← Back to Questions</Link>
      </div>

      {loading && <p className="qd-status">Loading…</p>}
      {!loading && err && <p className="qd-error">Error: {err}</p>}

      {!loading && !err && question && (
        <>
          <div className="qd-card">
            <div className="qd-row">
              <div className="qd-main">
                <p className="qd-question">{question.question}</p>
                <div className="qd-subtext">Topic #{question.topic_id}</div>
              </div>
              <span className="qd-badge">D{question.difficulty}</span>
            </div>
          </div>

          <form onSubmit={onSubmit} className="qd-form">
            <label className="qd-label">
              Your answer
              <textarea
                className="qd-input"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Type your solution…"
              />
            </label>

            <button type="submit" className="qd-submit" disabled={!canSubmit}>
              {submitting ? "Checking…" : "Submit"}
            </button>
          </form>

          {result && (
            <div className={`qd-result ${result.correct ? "qd-result--ok" : "qd-result--bad"}`}>
              <p className="qd-result-text">
                {result.correct ? "✅ Correct" : "❌ Incorrect"}
              </p>
              {result.feedback && <p className="qd-feedback">{result.feedback}</p>}
            </div>
          )}
        </>
      )}
    </div>
  );
}
