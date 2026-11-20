const pct = (x) => `${(x * 100).toFixed(1)}%`;

export default function TicketTable({ tickets, selectedId, onSelect }) {
  if (!tickets.length) {
    return <div className="card muted">Abhi koi ticket nahi hai.</div>;
  }
  return (
    <div className="card table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Message</th>
            <th>Category</th>
            <th>Urgency</th>
            <th>Confidence</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((t) => (
            <tr
              key={t.id}
              className={t.id === selectedId ? "active" : ""}
              onClick={() => onSelect(t.id)}
            >
              <td>{t.id}</td>
              <td className="msg">{t.message}</td>
              <td>{t.category}</td>
              <td>
                <span className={`badge urg-${t.urgency}`}>{t.urgency}</span>
              </td>
              <td>{pct(Math.min(t.category_conf, t.urgency_conf))}</td>
              <td>
                <span className={`badge st-${t.status}`}>{t.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
