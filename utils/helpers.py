import hashlib
from datetime import datetime


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_timestamp(ts: str | None):
    if not ts:
        return datetime.min
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return datetime.min
