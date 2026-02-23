from apps.api.app.db.session import SessionLocal
from apps.api.app.models import Case, Run


def test_list_runs_and_health(client):
    db = SessionLocal()
    try:
        case = Case(case_id="CASE-ABCDEFG1")
        db.add(case)
        db.add(
            Run(
                run_id="RUN-ABCDEFG1",
                case_id=case.case_id,
                pipeline="production",
                status="queued",
                progress=10,
                current_step="step1",
            )
        )
        db.commit()
    finally:
        db.close()

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    runs = client.get("/runs?limit=10")
    assert runs.status_code == 200
    assert runs.json()["items"][0]["run_id"] == "RUN-ABCDEFG1"
