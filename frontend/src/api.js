// VITE_API_URL build ke waqt bake hota hai, isliye change ke baad redeploy zaroori hai
const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  listTickets: () => request("/api/tickets"),
  stats: () => request("/api/stats"),
  createTicket: (message) =>
    request("/api/tickets", { method: "POST", body: JSON.stringify({ message }) }),
  updateTicket: (id, data) =>
    request(`/api/tickets/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
};
