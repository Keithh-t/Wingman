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

/** ---- Endpoint functions (co-located for now) ---- */
export async function getHealth(): Promise<Health> {
  const { data } = await api.get<Health>("/healthz");
  return data;
}

export async function getTopics(): Promise<Topic[]> {
  const { data } = await api.get<Topic[]>("/topics");
  return data;
}

/* Example for later:
export async function postAttempt(payload: { question_id: number; answer: string }) {
  const { data } = await api.post<{ status: string; score: number }>("/attempts", payload);
  return data;
}
*/
