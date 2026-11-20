export default function StatsCards({ stats }) {
  const items = [
    { label: "Total", value: stats?.total ?? "-" },
    { label: "Auto-replied", value: stats?.auto_replied ?? "-" },
    { label: "Escalated", value: stats?.escalated ?? "-" },
    { label: "Sent", value: stats?.sent ?? "-" },
  ];
  return (
    <div className="stats">
      {items.map((i) => (
        <div className="card" key={i.label}>
          <div className="muted">{i.label}</div>
          <div className="big">{i.value}</div>
        </div>
      ))}
    </div>
  );
}
