"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { StatusBadge } from "./StatusBadge";

const menus = [
  ["/", "Dashboard"],
  ["/cases", "Cases"],
  ["/runs", "Runs"],
  ["/learning", "Learning"],
  ["/settings", "Settings"],
] as const;

export function TopNav() {
  const pathname = usePathname();

  return (
    <div style={{ borderBottom: "1px solid #e6e6e6", background: "#fff" }}>
      <div className="container" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontWeight: 700 }}>Proposal Ops</div>
        <div style={{ display: "flex", gap: "0.4rem", alignItems: "center" }}>
          <StatusBadge label="MinIO OK" />
          <StatusBadge label="DB OK" />
          <StatusBadge label="Worker OK" />
          <StatusBadge label="Schema v1.0.0" />
        </div>
        <div style={{ display: "flex", gap: "1rem" }}>
          {menus.map(([href, label]) => (
            <Link key={href} href={href} className={`nav-link ${pathname === href ? "active" : ""}`}>
              {label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
