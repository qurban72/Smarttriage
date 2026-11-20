from openai import OpenAI

from app.config import DEEPSEEK_API_KEY

# DeepSeek OpenAI-compatible hai, isliye OpenAI SDK chalta hai
client = OpenAI(api_key=DEEPSEEK_API_KEY or "missing", base_url="https://api.deepseek.com")

SYSTEM = (
    "You are a customer support assistant. Answer ONLY using the FAQ context. "
    "If the context does not contain the answer, reply exactly: CANNOT_ANSWER. "
    "Keep the reply short, polite, and in the customer's language."
)


def draft_reply(ticket: str, faqs: list[dict]) -> str | None:
    context = "\n\n".join(f"Q: {f['question']}\nA: {f['answer']}" for f in faqs)
    resp = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"FAQ context:\n{context}\n\nTicket:\n{ticket}"},
        ],
    )
    text = (resp.choices[0].message.content or "").strip()
    return None if (not text or "CANNOT_ANSWER" in text) else text
