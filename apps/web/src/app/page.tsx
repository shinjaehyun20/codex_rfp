"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { DataTable } from "../components/DataTable";
import { api } from "../lib/api";
import type { RunItem } from "../lib/types";

export default function DashboardPage() {
  const [runs, setRuns] = useState<RunItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listRuns({ limit: 10 })
      .then((r) => setRuns(r.items ?? []))
      .catch((e) => setError(e.message ?? "failed"));
  }, []);

  const todayRuns = runs.length;
  const failedRuns = useMemo(() => runs.filter((x) => x.status === "failed").length, [runs]);
  const avgDuration = "-";

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <h1>Dashboard</h1>
      {error ? <div style={{ color: "crimson" }}>{error}</div> : null}

      <div className="grid-3">
        <div className="card"><div className="card-header">Today Runs</div><div className="card-body">{todayRuns}</div></div>
        <div className="card"><div className="card-header">Failed Runs</div><div className="card-body">{failedRuns}</div></div>
        <div className="card"><div className="card-header">Avg Duration</div><div className="card-body">{avgDuration} min</div></div>
      </div>

      <div className="row">
        <div className="card" style={{ flex: 1 }}>
          <div className="card-header">Recent Runs</div>
          <div className="card-body" style={{ padding: 0 }}>
            <DataTable
              headers={["Run ID", "Case ID", "Pipeline", "Status", "Progress", "Updated"]}
              rows={runs.map((r) => [
                <Link className="nav-link" href={`/runs/${r.run_id}`} key={`${r.run_id}-r`}>{r.run_id}</Link>,
                <Link className="nav-link" href={`/cases/${r.case_id}`} key={`${r.run_id}-c`}>{r.case_id}</Link>,
                r.pipeline,
                r.status,
                `${r.progress}%`,
                r.created_at,
              ])}
            />
          </div>
        </div>
        <div className="card" style={{ width: 260 }}>
          <div className="card-header">Actions</div>
          <div className="card-body actions" style={{ flexDirection: "column" }}>
            <Link href="/cases" className="button">New Case</Link>
            <Link href="/learning" className="button">Upload Winning Case</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
