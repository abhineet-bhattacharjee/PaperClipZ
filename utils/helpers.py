import hashlib
import math
from datetime import datetime


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_timestamp(ts: str | None) -> datetime:
    if not ts:
        return datetime.min
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return datetime.min


def calculate_score(entry: dict) -> float:
    now = datetime.now()

    timestamp = (
        entry.get("last_pasted_at")
        or entry.get("last_copied_at")
        or entry.get("created_at")
    )

    dt = parse_timestamp(timestamp)
    if dt == datetime.min:
        return 0.0

    hours_ago = (now - dt).total_seconds() / 3600
    recency = math.exp(-hours_ago / 24)
    frequency = math.log(entry.get("paste_count", 0) + 1)

    return (recency * 10) + (frequency * 2 * recency)