"use client";

import { ReactNode, useState } from "react";

export function Tabs({ tabs }: { tabs: Array<{ name: string; content: ReactNode }> }) {
  const [idx, setIdx] = useState(0);
  return (
    <div className="card">
      <div className="card-header" style={{ display: "flex", gap: "0.5rem" }}>
        {tabs.map((tab, i) => (
          <button key={tab.name} className="button" onClick={() => setIdx(i)} style={{ fontWeight: idx === i ? 700 : 400 }}>
            {tab.name}
          </button>
        ))}
      </div>
      <div className="card-body">{tabs[idx]?.content}</div>
    </div>
  );
}
