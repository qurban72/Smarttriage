# SmartTriage

AI-powered support ticket classifier, FAQ retrieval responder, confidence gating and dashboard.

Stack: FastAPI, PostgreSQL, DistilBERT (Hugging Face), Google Gemini embeddings, Pinecone, DeepSeek, React + Vite, Docker, Railway.

## Local run (Docker)

1. `cp backend/.env.example backend/.env` and fill in the keys.
2. Train the models once (see below) and set `CATEGORY_MODEL` / `URGENCY_MODEL` to your Hugging Face repos.
3. `python backend/scripts/ingest_faqs.py` (needs backend/.env loaded, or run it inside the backend container).
4. `docker compose up --build`
5. Dashboard: http://localhost:8080 · API docs: http://localhost:8000/docs

## Training

```bash
cd backend
pip install -r requirements-train.txt
python scripts/train_classifier.py --hf-user your-hf-username
```

Replace `data/tickets.csv` with a real dataset (100-200 rows per category minimum).

## Deploy to Railway

See the deploy section in the project guide. Summary: one PostgreSQL service, one backend service (Root Directory `backend`), one frontend service (Root Directory `frontend`, variable `VITE_API_URL` set to the backend URL).
