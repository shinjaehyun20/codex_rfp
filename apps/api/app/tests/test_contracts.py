import json
from pathlib import Path

from jsonschema import validate

SCHEMA_DIR = Path("contracts/schemas")


def load_schema(name: str):
    return json.loads((SCHEMA_DIR / name).read_text())


def test_contract_schemas_validate_minimum_samples():
    samples = {
        "envelope.v1.schema.json": {"type": "rfp.meta.v1", "schema_version": "v1", "run_id": "RUN-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "payload": {}},
        "artifact.v1.schema.json": {"type": "artifact.v1", "schema_version": "v1", "artifact_id": "ART-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "uri": "s3://bucket/a", "sha256": "a" * 64, "role": "input", "mime": "application/pdf"},
        "stateref.v1.schema.json": {"type": "stateref.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "state_type": "rfp.meta.v1", "uri": "s3://bucket/s", "sha256": "b" * 64},
        "rfp.meta.v1.schema.json": {"type": "rfp.meta.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "source_artifact_id": "ART-ABCDEFG1", "filename": "a.pdf"},
        "rfp.parsed.v1.schema.json": {"type": "rfp.parsed.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "artifact_id": "ART-ABCDEFG1", "metadata": {"page_count": 1, "is_scanned": False, "ocr_applied": False}, "text_blocks": [{"page": 1, "block_id": "b1", "text": "hello"}]},
        "requirements.v1.schema.json": {"type": "requirements.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "items": [{"requirement_id": "REQ-ABCDEFG1", "kind": "mandatory", "text": "필수", "source": {"artifact_id": "ART-ABCDEFG1", "page": 1, "block_id": "b1"}}]},
        "evaluation.v1.schema.json": {"type": "evaluation.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "sum_score": 100, "criteria": [{"criterion_id": "SEC-ABCDEFG1", "title": "점수", "score": 100}]},
        "mapping.v1.schema.json": {"type": "mapping.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "mappings": [{"requirement_id": "REQ-ABCDEFG1", "section_id": "SEC-ABCDEFG1"}]},
        "proposal.draft.v1.schema.json": {"type": "proposal.draft.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "sections": [{"section_id": "SEC-ABCDEFG1", "title": "개요", "content": "내용"}]},
        "compliance.v1.schema.json": {"type": "compliance.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "hard_fail": False, "findings": [{"level": "info", "message": "ok"}]},
        "case.analysis.v1.schema.json": {"type": "case.analysis.v1", "schema_version": "v1", "state_id": "STATE-ABCDEFG1", "case_id": "CASE-ABCDEFG1", "status": "WIN", "delta": {"summary": "win"}},
    }

    for file_name, sample in samples.items():
        validate(instance=sample, schema=load_schema(file_name))
