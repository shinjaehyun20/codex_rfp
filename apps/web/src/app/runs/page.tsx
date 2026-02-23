"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { DataTable } from "../../components/DataTable";
import { api } from "../../lib/api";
import type { RunItem } from "../../lib/types";

export default function RunsPage() {
  const [items, setItems] = useState<RunItem[]>([]);
  const [pipeline, setPipeline] = useState("");
  const [status, setStatus] = useState("");

  const reload = () => api.listRuns({ pipeline: pipeline || undefined, status: status || undefined }).then((r) => setItems(r.items));

  useEffect(() => {
    reload();
  }, []);

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <h1>Runs</h1>
      <div className="actions">
        <select className="select" value={pipeline} onChange={(e) => setPipeline(e.target.value)}>
          <option value="">pipeline: all</option>
          <option value="production">production</option>
          <option value="learning">learning</option>
          <option value="comparison">comparison</option>
        </select>
        <select className="select" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">status: all</option>
          <option value="queued">queued</option>
          <option value="running">running</option>
          <option value="completed">completed</option>
          <option value="failed">failed</option>
        </select>
        <button className="button" onClick={reload}>Apply</button>
      </div>

      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          <DataTable
            headers={["Run ID", "Case ID", "Pipeline", "Step", "Progress", "Status", "Created"]}
            rows={items.map((r) => [
              <Link href={`/runs/${r.run_id}`} key={r.run_id}>{r.run_id}</Link>,
              <Link href={`/cases/${r.case_id}`} key={`${r.run_id}-case`}>{r.case_id}</Link>,
              r.pipeline,
              r.current_step,
              `${r.progress}%`,
              r.status,
              r.created_at,
            ])}
          />
        </div>
      </div>
    </div>
  );
}
