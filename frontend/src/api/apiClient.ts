import axios from "axios";
import { API_BASE_URL, API_TIMEOUT_MS } from "../config/apiConfig";

/** Axios instance */
export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT_MS,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg =
      err.response?.data?.message ||
      err.message ||
      "Request failed";
    return Promise.reject(new Error(msg));
  }
);

/** ---- Types (keep simple here; move to /types later if it grows) ---- */
export type Health = { status: string };
export type Topic  = { id: number; slug: string; name: string };
export type Question = {
  id: number;
  topic_id: number;
  difficulty: number;
  question: string;
};
export type QuestionDetail = Question;

export type AttemptPost = {
  question_id: number;
  user_answer: string;
};

export type AttemptResult = {
  correct: boolean;
  feedback?: string | null;
};

// ai suggested
export type RequestOptions = { signal?: AbortSignal };





/** ---- Endpoint functions (co-located for now) ---- */
export async function getHealth(): Promise<Health> {
  const { data } = await api.get<Health>("/healthz");
  return data;
}

export async function getTopics(): Promise<Topic[]> {
  const { data } = await api.get<Topic[]>("/topics");
  return data;
}

export async function getQuestions(params: { topic_id?: number },
   options?: RequestOptions): Promise<Question[]> {
  const { data } = await api.get<Question[]>("/questions", { params, signal: options?.signal });
  return data;
}

/** Fetch detailed info for a question by ID */
export async function getQuestionById(id: number, options?: RequestOptions): Promise<QuestionDetail> {
  const { data } = await api.get<QuestionDetail>(`/questions/${id}`, { signal: options?.signal });
  return data;
}

/** Submit an attempt for a question */
export async function postAttempt(payload: AttemptPost, options?: RequestOptions): Promise<AttemptResult> {
  const { data } = await api.post<AttemptResult>("/attempts", payload, { signal: options?.signal });
  return data;
}

/* Example for later:
export async function postAttempt(payload: { question_id: number; answer: string }) {
  const { data } = await api.post<{ status: string; score: number }>("/attempts", payload);
  return data;
}
*/


// /** Query keys for react-query - AI suggestion, check on it later*/
// export const QK = {
//   topics: ["topics"] as const,
//   questions: (topic_id?: number) => ["questions", { topic_id }] as const,
//   question: (id: number) => ["question", id] as const,
// };
