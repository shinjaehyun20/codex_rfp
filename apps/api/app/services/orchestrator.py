import hashlib
import json
from sqlalchemy.orm import Session

from apps.api.app.models import Run, State
from apps.api.app.pipelines.production import get_steps
from apps.api.app.services.ids import make_id


def run_production_pipeline(db: Session, run_id: str):
    run = db.get(Run, run_id)
    if not run:
        raise ValueError("Run not found")

    run.status = "running"
    run.current_step = "starting"
    db.commit()

    envelope = {
        "type": "envelope.v1",
        "schema_version": "v1",
        "run_id": run.run_id,
        "case_id": run.case_id,
        "payload": {},
    }

    steps = get_steps()
    for idx, step in enumerate(steps, start=1):
        run.current_step = step.__name__
        envelope = step(envelope)

        if idx == len(steps):
            state_json = {
                "type": "rfp.meta.v1",
                "schema_version": "v1",
                "state_id": envelope["payload"]["state_id"],
                "case_id": run.case_id,
                "source_artifact_id": envelope["payload"].get("artifact_id", "ART-00000000"),
                "filename": "dummy.txt",
            }
            body = json.dumps(state_json, ensure_ascii=False).encode()
            sha = hashlib.sha256(body).hexdigest()
            state = State(
                state_id=state_json["state_id"],
                case_id=run.case_id,
                uri=f"s3://states/{state_json['state_id']}.json",
                sha256=sha,
                type=state_json["type"],
            )
            db.add(state)

        run.progress = round((idx / len(steps)) * 100, 2)
        db.commit()

    run.status = "completed"
    run.current_step = "done"
    db.commit()
