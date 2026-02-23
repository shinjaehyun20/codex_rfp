"use client";

import { useEffect, useState } from "react";
import { api } from "../../lib/api";

export default function SettingsPage() {
  const [status, setStatus] = useState<Record<string, string>>({});

  useEffect(() => {
    api.health().then((v) => setStatus(v));
  }, []);

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <h1>Settings</h1>
      <div className="card"><div className="card-body" style={{ display: "grid", gap: "0.4rem" }}>
        <div>Schema Version: {status.schema_version ?? "-"}</div>
        <div>Storage Endpoint: {process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}</div>
        <div>DB Connected: {status.db ?? "-"}</div>
        <div>Worker Connected: {status.worker ?? "-"}</div>
        <div>LLM Provider: (v1 placeholder)</div>
      </div></div>
    </div>
  );
}
