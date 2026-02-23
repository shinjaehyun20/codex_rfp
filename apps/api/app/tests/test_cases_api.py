from io import BytesIO

from apps.worker.worker.tasks import run_pipeline_task


def test_create_case_upload_works(client, monkeypatch):
    monkeypatch.setattr(run_pipeline_task, "delay", lambda run_id: None)
    files = [
        ("files", ("rfp.txt", BytesIO(b"hello rfp"), "text/plain")),
    ]
    response = client.post("/cases", files=files)
    assert response.status_code == 200
    body = response.json()
    assert body["case_id"].startswith("CASE-")
    assert len(body["artifact_ids"]) == 1
