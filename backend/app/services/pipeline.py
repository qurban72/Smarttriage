from app.config import CATEGORY_MODEL, URGENCY_MODEL, CONF_CLASSIFIER, CONF_RETRIEVAL
from app.services.classifier import predict, CATEGORY_LABELS, URGENCY_LABELS
from app.services.retrieval import search_faqs
from app.services.responder import draft_reply


def process_ticket(text: str) -> dict:
    category, cat_conf = predict(text, CATEGORY_MODEL, candidate_labels=CATEGORY_LABELS)
    urgency, urg_conf = predict(text, URGENCY_MODEL, candidate_labels=URGENCY_LABELS)
    faqs = search_faqs(text)
    top_score = faqs[0]["score"] if faqs else 0.0

    # Confidence gating
    low_confidence = (
        cat_conf < CONF_CLASSIFIER
        or urg_conf < CONF_CLASSIFIER
        or top_score < CONF_RETRIEVAL
    )
    high_urgency = urgency == "high"  # high urgency hamesha human ke paas jaye

    draft = None
    if not low_confidence and not high_urgency:
        draft = draft_reply(text, faqs)

    return {
        "category": category,
        "category_conf": cat_conf,
        "urgency": urgency,
        "urgency_conf": urg_conf,
        "retrieval_score": top_score,
        "suggested_reply": draft,
        "status": "auto_replied" if draft else "escalated",
    }
