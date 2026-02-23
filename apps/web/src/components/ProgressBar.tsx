export function ProgressBar({ value }: { value: number }) {
  const pct = Math.max(0, Math.min(100, Math.round(value)));
  return (
    <div style={{ width: "100%", border: "1px solid #ddd", borderRadius: 9999, overflow: "hidden", background: "#f2f2f2" }}>
      <div style={{ width: `${pct}%`, background: "#2f6feb", color: "white", fontSize: "0.75rem", padding: "0.1rem 0.4rem" }}>{pct}%</div>
    </div>
  );
}
