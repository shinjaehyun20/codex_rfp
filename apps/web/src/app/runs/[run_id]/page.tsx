"use client";

import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { ProgressBar } from "../../../components/ProgressBar";
import { Tabs } from "../../../components/Tabs";
import { api } from "../../../lib/api";
import { poll } from "../../../lib/polling";
import type { RunDetailResponse } from "../../../lib/types";

export default function RunDetailPage() {
  const { run_id } = useParams<{ run_id: string }>();
  const [detail, setDetail] = useState<RunDetailResponse | null>(null);

  useEffect(() => {
    const stop = poll(
      () => api.getRun(run_id),
      (v) => v.status === "queued" || v.status === "running",
      3000,
      (v) => setDetail(v)
    );
    return stop;
  }, [run_id]);

  const stepsRows = useMemo(() => {
    if (!detail) return [];
    return [[detail.current_step, "-", "-", detail.status, detail.errors.join("; ") || "-"]];
  }, [detail]);

  if (!detail) return <div>Loading...</div>;

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <h1>Run Detail: {detail.run_id}</h1>
      <div className="card"><div className="card-body" style={{ display: "grid", gap: "0.5rem" }}>
        <div>Case ID: {detail.case_id}</div>
        <div>Pipeline: {detail.pipeline}</div>
        <div>Status: {detail.status}</div>
        <ProgressBar value={detail.progress} />
        <div>Current Step: {detail.current_step}</div>
        <button className="button" disabled>Cancel (v1)</button>
      </div></div>

      <Tabs
        tabs={[
          {
            name: "Steps",
            content: <pre style={{ margin: 0 }}>{JSON.stringify(stepsRows, null, 2)}</pre>,
          },
          {
            name: "States",
            content: <pre style={{ margin: 0 }}>{JSON.stringify(detail.state_refs, null, 2)}</pre>,
          },
          {
            name: "Artifacts",
            content: <pre style={{ margin: 0 }}>{JSON.stringify(detail.artifacts, null, 2)}</pre>,
          },
        ]}
      />
    </div>
  );
}
