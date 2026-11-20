from google import genai
from google.genai import types
from pinecone import Pinecone

from app.config import GOOGLE_API_KEY, PINECONE_API_KEY, PINECONE_INDEX

# Client ko lazily banate hain taake empty key par import hi na toote
_genai_client = None
_index = None


def _get_genai():
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(api_key=GOOGLE_API_KEY or None)
    return _genai_client


def _get_index():
    global _index
    if _index is None:
        _index = Pinecone(api_key=PINECONE_API_KEY).Index(PINECONE_INDEX)
    return _index


def embed(texts: list[str], task_type: str) -> list[list[float]]:
    res = _get_genai().models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task_type,        # RETRIEVAL_DOCUMENT ya RETRIEVAL_QUERY
            output_dimensionality=768,  # Pinecone index bhi 768 ka hona chahiye
        ),
    )
    return [e.values for e in res.embeddings]


def search_faqs(query: str, top_k: int = 3) -> list[dict]:
    vec = embed([query], "RETRIEVAL_QUERY")[0]
    res = _get_index().query(vector=vec, top_k=top_k, include_metadata=True)
    return [{"id": m.id, "score": m.score, **(m.metadata or {})} for m in res.matches]
