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
      err.response?.data?.detail ||
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

export type AuthResponse = {
  token: string;
  user_id: number;
  email: string;
  username: string;
};

export type MeResponse = {
  user_id: number;
  email: string;
  username: string;
};




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


// Progress items

export type ProgressItem = {
  question_id: number;
  user_answer: string;
  correct: boolean;
  attempted_at: string;
};

export type ProgressResponse = {
  accuracy: number;
  attempts: ProgressItem[];
};

export async function getProgress(limit =20, options?: RequestOptions) {
  const { data } = await api.get<ProgressResponse>("/progress", {
    params: { limit },
    signal: options?.signal,
  });
  return data;
}

// Authentication

export async function register(payload: { email: string; username: string; password: string }) {
  const { data } = await api.post<AuthResponse>("/register", payload);
  return data;
}

export async function login(payload: { email: string; password: string }) {
  const { data } = await api.post<AuthResponse>("/login", payload);
  return data;
}

export async function fetchMe() : Promise<MeResponse> {
  const { data } = await api.get<MeResponse>("/me");
  return data;
}

export async function logout() {
  await api.post("/logout");
}
