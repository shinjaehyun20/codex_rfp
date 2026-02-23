from typing import List, Literal, Optional
from pydantic import BaseModel

class CaseCreateResponse(BaseModel):
    case_id: str
    artifact_ids: List[str]

class RunCreateRequest(BaseModel):
    case_id: str
    pipeline: Literal["production", "learning", "comparison"]
    proposal_profile_id: Optional[str] = None

class RunCreateResponse(BaseModel):
    run_id: str

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
