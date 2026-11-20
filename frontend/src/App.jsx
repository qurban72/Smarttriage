import { useCallback, useEffect, useState } from "react";
import { api } from "./api";
import StatsCards from "./components/StatsCards";
import TicketForm from "./components/TicketForm";
import TicketTable from "./components/TicketTable";
import TicketDetail from "./components/TicketDetail";

export default function App() {
  const [tickets, setTickets] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      const [t, s] = await Promise.all([api.listTickets(), api.stats()]);
      setTickets(t);
      setStats(s);
      setError("");
    } catch (e) {
      setError(`Backend se connect nahi ho paa raha: ${e.message}`);
    }
  }, []);

  useEffect(() => {
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [load]);

  const selected = tickets.find((t) => t.id === selectedId) || null;

  return (
    <div className="container">
      <header>
        <h1>SmartTriage</h1>
        <p className="muted">Support tickets: classification, auto-reply aur escalation</p>
      </header>

      {error && <div className="error">{error}</div>}

      <StatsCards stats={stats} />

      <TicketForm
        onCreated={async (ticket) => {
          await load();
          setSelectedId(ticket.id);
        }}
      />

      <div className="layout">
        <TicketTable tickets={tickets} selectedId={selectedId} onSelect={setSelectedId} />
        {selected && <TicketDetail key={selected.id} ticket={selected} onUpdated={load} />}
      </div>
    </div>
  );
}
