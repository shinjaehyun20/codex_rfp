export type RunStatus = "queued" | "running" | "completed" | "failed";

export type RunItem = {
  run_id: string;
  case_id: string;
  pipeline: string;
  status: RunStatus | string;
  progress: number;
  current_step: string;
  created_at: string;
};

export type RunsListResponse = { items: RunItem[] };

export type CaseItem = {
  case_id: string;
  documents: number;
  last_run_status: string | null;
  bid_status: "WIN" | "LOSE" | "UNKNOWN" | string;
  created_at: string;
};

export type CasesListResponse = { items: CaseItem[] };

export type RunDetailResponse = {
  run_id: string;
  case_id: string;
  pipeline: string;
  status: string;
  progress: number;
  current_step: string;
  artifacts: Array<{ artifact_id: string; filename?: string; uri: string; type: string; role: string }>;
  state_refs: Array<{ state_id: string; uri: string; type: string }>;
  errors: string[];
};

export type CaseDetailResponse = {
  case_id: string;
  bid_status: string;
  bid_score?: string | null;
  artifacts: Array<{ artifact_id: string; filename: string; uri: string; type: string; role: string; uploaded: string }>;
  recent_runs: Array<{ run_id: string; pipeline: string; status: string; progress: number; created_at: string }>;
};
