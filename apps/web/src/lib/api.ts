import type { CaseDetailResponse, CasesListResponse, RunDetailResponse, RunsListResponse } from "./types";

export type ApiError = { message: string; status?: number };

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw { message: text || `HTTP ${res.status}`, status: res.status } as ApiError;
  }

  return (await res.json()) as T;
}

export const api = {
  listRuns: (params?: { limit?: number; pipeline?: string; status?: string }) => {
    const qs = new URLSearchParams();
    if (params?.limit) qs.set("limit", String(params.limit));
    if (params?.pipeline) qs.set("pipeline", params.pipeline);
    if (params?.status) qs.set("status", params.status);
    const s = qs.toString();
    return request<RunsListResponse>(`/runs${s ? `?${s}` : ""}`);
  },

  getRun: (runId: string) => request<RunDetailResponse>(`/runs/${encodeURIComponent(runId)}`),

  listCases: (params?: { q?: string }) => {
    const qs = new URLSearchParams();
    if (params?.q) qs.set("q", params.q);
    const s = qs.toString();
    return request<CasesListResponse>(`/cases${s ? `?${s}` : ""}`);
  },

  getCase: (caseId: string) => request<CaseDetailResponse>(`/cases/${encodeURIComponent(caseId)}`),

  createCase: (body?: { bid_status?: "WIN" | "LOSE" | "UNKNOWN"; bid_score?: number }) => {
    const form = new FormData();
    if (body?.bid_status) form.append("bid_status", body.bid_status);
    if (body?.bid_score !== undefined) form.append("bid_score", String(body.bid_score));
    return fetch(`${baseUrl}/cases`, { method: "POST", body: form }).then(async (res) => {
      if (!res.ok) throw { message: await res.text(), status: res.status } as ApiError;
      return res.json();
    });
  },

  uploadArtifactsToCase: async (caseId: string, files: File[]) => {
    const form = new FormData();
    for (const f of files) form.append("files", f);
    const res = await fetch(`${baseUrl}/cases/${encodeURIComponent(caseId)}/artifacts`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) throw { message: await res.text(), status: res.status } as ApiError;
    return (await res.json()) as { case_id: string; artifact_ids: string[] };
  },

  createRun: (body: { case_id: string; pipeline: string; proposal_profile_id?: string }) =>
    request<{ run_id: string }>(`/runs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),

  health: () => request<{ status: string; schema_version: string; db: string; storage: string; worker: string }>(`/health`),
};
