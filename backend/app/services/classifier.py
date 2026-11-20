from huggingface_hub import InferenceClient
from app.config import HF_TOKEN

_cache: dict = {}

# Labels derived from training data
CATEGORY_LABELS = ["billing", "technical", "account", "shipping"]
URGENCY_LABELS = ["low", "medium", "high"]


def _load(model_name: str) -> InferenceClient:
    if model_name not in _cache:
        _cache[model_name] = InferenceClient(model=model_name, token=HF_TOKEN or None)
    return _cache[model_name]


def predict(text: str, model_name: str, candidate_labels: list[str] | None = None) -> tuple[str, float]:
    """Run zero-shot classification via HuggingFace Inference API."""
    client = _load(model_name)
    if candidate_labels is None:
        candidate_labels = CATEGORY_LABELS
    result = client.zero_shot_classification(text, labels=candidate_labels)
    # Result is a list of dicts with 'label' and 'score', sorted by score desc
    top = result[0]
    return top["label"], float(top["score"])
