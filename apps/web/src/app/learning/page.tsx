"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { DataTable } from "../../components/DataTable";
import { api } from "../../lib/api";
import type { CaseItem } from "../../lib/types";

export default function LearningPage() {
  const [items, setItems] = useState<CaseItem[]>([]);

  useEffect(() => {
    api.listCases().then((r) => setItems(r.items.filter((x) => x.bid_status !== "UNKNOWN")));
  }, []);

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <h1>Learning</h1>
      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          <DataTable
            headers={["Case ID", "Status", "Alignment Score", "Strength Patterns", "Weakness Patterns", "Updated"]}
            rows={items.map((c) => [
              <Link href={`/cases/${c.case_id}`} key={c.case_id}>{c.case_id}</Link>,
              c.bid_status,
              "-",
              "-",
              "-",
              c.created_at,
            ])}
          />
        </div>
      </div>
    </div>
  );
}
