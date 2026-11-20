import { useState } from "react";
import { api } from "../api";

const pct = (x) => `${(x * 100).toFixed(1)}%`;

export default function TicketDetail({ ticket, onUpdated }) {
  const [reply, setReply] = useState(ticket.suggested_reply ?? "");
  const [saving, setSaving] = useState(false);

  async function approve() {
    setSaving(true);
    try {
      await api.updateTicket(ticket.id, { status: "sent", suggested_reply: reply });
      onUpdated();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="card detail">
      <h2>Ticket #{ticket.id}</h2>
      <p className="msg-full">{ticket.message}</p>

      <dl>
        <dt>Category</dt>
        <dd>{ticket.category} ({pct(ticket.category_conf)})</dd>
        <dt>Urgency</dt>
        <dd>{ticket.urgency} ({pct(ticket.urgency_conf)})</dd>
        <dt>Retrieval score</dt>
        <dd>{pct(ticket.retrieval_score)}</dd>
        <dt>Status</dt>
        <dd>{ticket.status}</dd>
      </dl>

      <label>{ticket.suggested_reply ? "Suggested reply" : "Reply (manually likhein)"}</label>
      <textarea
        rows={6}
        value={reply}
        onChange={(e) => setReply(e.target.value)}
        disabled={ticket.status === "sent"}
        placeholder="Escalated ticket hai, reply khud likhein..."
      />

      {ticket.status !== "sent" ? (
        <button onClick={approve} disabled={saving || !reply.trim()}>
          {saving ? "Saving..." : "Approve & Send"}
        </button>
      ) : (
        <p className="muted">Ye ticket already send ho chuka hai.</p>
      )}
    </div>
  );
}
