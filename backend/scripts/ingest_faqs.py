"""
Usage (backend folder se, env vars set hon):
    python scripts/ingest_faqs.py

faqs.json ko embed karke Pinecone mein upsert karta hai.
"""
import json
import os
import sys

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv  # noqa: E402

load_dotenv(os.path.join(BASE_DIR, ".env"))

from app.services.retrieval import embed, _get_index  # noqa: E402

BATCH = 50


def main():
    with open(os.path.join(BASE_DIR, "data", "faqs.json"), encoding="utf-8") as f:
        faqs = json.load(f)

    index = _get_index()
    total = 0
    for i in range(0, len(faqs), BATCH):
        batch = faqs[i : i + BATCH]
        texts = [f"{x['question']}\n{x['answer']}" for x in batch]
        vectors = embed(texts, "RETRIEVAL_DOCUMENT")
        index.upsert(
            vectors=[
                {
                    "id": x["id"],
                    "values": v,
                    "metadata": {"question": x["question"], "answer": x["answer"]},
                }
                for x, v in zip(batch, vectors)
            ]
        )
        total += len(batch)
        print(f"Upserted {total}/{len(faqs)}")

    print("Done.")


if __name__ == "__main__":
    main()
