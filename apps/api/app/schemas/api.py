from typing import List, Literal, Optional
from pydantic import BaseModel


class CaseCreateRequest(BaseModel):
    bid_status: Literal["WIN", "LOSE", "UNKNOWN"] = "UNKNOWN"
    bid_score: Optional[float] = None


class CaseCreateResponse(BaseModel):
    case_id: str
    artifact_ids: List[str]


class CaseItemResponse(BaseModel):
    case_id: str
    documents: int
    last_run_status: Optional[str]
    bid_status: str
    created_at: str


class CasesListResponse(BaseModel):
    items: List[CaseItemResponse]


class CaseDetailResponse(BaseModel):
    case_id: str
    bid_status: str
    bid_score: Optional[str]
    artifacts: List[dict]
    recent_runs: List[dict]


class RunCreateRequest(BaseModel):
    case_id: str
    pipeline: Literal["production", "learning", "comparison"]
    proposal_profile_id: Optional[str] = None


class RunCreateResponse(BaseModel):
    run_id: str


class RunItemResponse(BaseModel):
    run_id: str
    case_id: str
    pipeline: str
    status: str
    progress: float
    current_step: str
    created_at: str


class RunsListResponse(BaseModel):
    items: List[RunItemResponse]


class RunStatusResponse(BaseModel):
    run_id: str
    case_id: str
    pipeline: str
    status: str
    progress: float
    current_step: str
    artifacts: List[dict]
    state_refs: List[dict]
    errors: List[str]


class HealthResponse(BaseModel):
    status: str
    schema_version: str
    db: str
    storage: str
    worker: str
