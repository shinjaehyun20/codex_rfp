from io import BytesIO

from apps.worker.worker.tasks import run_pipeline_task


def test_create_case_upload_works(client, monkeypatch):
    monkeypatch.setattr(run_pipeline_task, "delay", lambda run_id: None)
    files = [("files", ("rfp.txt", BytesIO(b"hello rfp"), "text/plain"))]
    response = client.post("/cases", files=files)
    assert response.status_code == 200
    body = response.json()
    assert body["case_id"].startswith("CASE-")
    assert len(body["artifact_ids"]) == 1


def test_list_cases_and_upload_existing_case(client, monkeypatch):
    monkeypatch.setattr(run_pipeline_task, "delay", lambda run_id: None)

    create_resp = client.post("/cases")
    assert create_resp.status_code == 200
    case_id = create_resp.json()["case_id"]

    upload_resp = client.post(
        f"/cases/{case_id}/artifacts",
        files=[("files", ("appendix.pdf", BytesIO(b"pdf-bytes"), "application/pdf"))],
    )
    assert upload_resp.status_code == 200
    assert len(upload_resp.json()["artifact_ids"]) == 1

    list_resp = client.get("/cases")
    assert list_resp.status_code == 200
    items = list_resp.json()["items"]
    assert any(x["case_id"] == case_id for x in items)

    detail_resp = client.get(f"/cases/{case_id}")
    assert detail_resp.status_code == 200
    assert len(detail_resp.json()["artifacts"]) == 1
