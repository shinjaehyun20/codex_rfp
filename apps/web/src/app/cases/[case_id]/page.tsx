"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { DataTable } from "../../../components/DataTable";
import { DropzoneUpload } from "../../../components/DropzoneUpload";
import { api } from "../../../lib/api";
import type { CaseDetailResponse } from "../../../lib/types";

export default function CaseDetailPage() {
  const { case_id } = useParams<{ case_id: string }>();
  const router = useRouter();
  const [detail, setDetail] = useState<CaseDetailResponse | null>(null);
  const [pipeline, setPipeline] = useState("production");
  const [profile, setProfile] = useState("public-tech-v1");

  const load = () => api.getCase(case_id).then(setDetail);

  useEffect(() => {
    load();
  }, [case_id]);

  if (!detail) return <div>Loading...</div>;

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <h1>Case Detail: {detail.case_id}</h1>

      <div className="card">
        <div className="card-header">Bid Result</div>
        <div className="card-body actions">
          <select className="select" defaultValue={detail.bid_status}>
            <option>WIN</option><option>LOSE</option><option>UNKNOWN</option>
          </select>
          <input className="input" placeholder="Score(optional)" defaultValue={detail.bid_score ?? ""} />
          <button className="button" disabled>Save (v1)</button>
        </div>
      </div>

      <DropzoneUpload onUpload={async (files) => { await api.uploadArtifactsToCase(case_id, files); await load(); }} />

      <div className="card">
        <div className="card-header">Artifacts</div>
        <div className="card-body" style={{ padding: 0 }}>
          <DataTable
            headers={["Artifact ID", "Filename", "Type", "Role", "Uploaded", "Actions"]}
            rows={detail.artifacts.map((a) => [a.artifact_id, a.filename, a.type, a.role, a.uploaded, <a key={a.artifact_id} href={a.uri} target="_blank">Download</a>])}
          />
        </div>
      </div>

      <div className="card">
        <div className="card-header">Run Pipeline</div>
        <div className="card-body actions">
          <select className="select" value={pipeline} onChange={(e) => setPipeline(e.target.value)}>
            <option value="production">production</option>
            <option value="learning">learning</option>
          </select>
          <input className="input" value={profile} onChange={(e) => setProfile(e.target.value)} />
          <button
            className="button"
            onClick={async () => {
              const res = await api.createRun({ case_id, pipeline, proposal_profile_id: profile });
              router.push(`/runs/${res.run_id}`);
            }}
          >
            Run Pipeline
          </button>
        </div>
      </div>

      <div className="card">
        <div className="card-header">Recent Runs</div>
        <div className="card-body" style={{ display: "grid", gap: "0.5rem" }}>
          {detail.recent_runs.map((r) => (
            <Link key={r.run_id} href={`/runs/${r.run_id}`}>{r.run_id} - {r.status} ({r.progress}%)</Link>
          ))}
        </div>
      </div>
    </div>
  );
}
