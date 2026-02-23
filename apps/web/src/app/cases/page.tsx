"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { DataTable } from "../../components/DataTable";
import { api } from "../../lib/api";
import type { CaseItem } from "../../lib/types";

export default function CasesPage() {
  const [q, setQ] = useState("");
  const [items, setItems] = useState<CaseItem[]>([]);

  const reload = () => api.listCases({ q: q || undefined }).then((r) => setItems(r.items));

  useEffect(() => {
    reload();
  }, []);

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <h1>Cases</h1>
      <div className="actions">
        <input className="input" placeholder="case_id 검색" value={q} onChange={(e) => setQ(e.target.value)} />
        <button className="button" onClick={reload}>Search</button>
        <button className="button" onClick={() => api.createCase({ bid_status: "UNKNOWN" }).then(reload)}>Create Case</button>
      </div>

      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          <DataTable
            headers={["Case ID", "Documents", "Last Run Status", "Bid Status", "Created"]}
            rows={items.map((c) => [
              <Link href={`/cases/${c.case_id}`} key={c.case_id}>{c.case_id}</Link>,
              String(c.documents),
              c.last_run_status ?? "-",
              c.bid_status,
              c.created_at,
            ])}
          />
        </div>
      </div>
    </div>
  );
}
