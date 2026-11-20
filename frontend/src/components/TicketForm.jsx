import { useState } from "react";
import { api } from "../api";

export default function TicketForm({ onCreated }) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function submit(e) {
    e.preventDefault();
    if (message.trim().length < 3) return;
    setLoading(true);
    setErr("");
    try {
      const ticket = await api.createTicket(message.trim());
      setMessage("");
      onCreated(ticket);
    } catch (ex) {
      setErr(ex.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card form" onSubmit={submit}>
      <label>Naya ticket</label>
      <textarea
        rows={3}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Customer ka message yahan paste karein..."
      />
      <div className="row">
        <button type="submit" disabled={loading}>
          {loading ? "Process ho raha hai..." : "Classify karein"}
        </button>
        {err && <span className="error-inline">{err}</span>}
      </div>
    </form>
  );
}
