export function StatusBadge({ label, ok = true }: { label: string; ok?: boolean }) {
  return <span className="badge" style={{ background: ok ? "#eefcf0" : "#fdecec" }}>{label}</span>;
}
