import math
from datetime import datetime
from utils.helpers import parse_timestamp


class ClipboardManager:
    def __init__(self, storage, sort_mode: str = "smart"):
        self.storage = storage
        self.sort_mode = sort_mode

    def _calculate_score(self, entry: dict) -> float:
        now = datetime.now()

        last_pasted = entry.get("last_pasted_at")
        last_copied = entry.get("last_copied_at")
        created = entry.get("created_at")

        if last_pasted:
            timestamp = last_pasted
        elif last_copied:
            timestamp = last_copied
        else:
            timestamp = created

        dt = parse_timestamp(timestamp)

        if dt == datetime.min:
            return 0.0

        hours_ago = (now - dt).total_seconds() / 3600
        recency_score = math.exp(-hours_ago / 24)

        paste_count = entry.get("paste_count", 0)
        frequency_score = math.log(paste_count + 1)

        return (recency_score * 10) + (frequency_score * 2 * recency_score)

    def get_sorted_items(self, limit: int = 10) -> list[dict]:
        pinned = [e for e in self.storage.history if e.get("pinned")]
        unpinned = [e for e in self.storage.history if not e.get("pinned")]

        pinned.sort(key=lambda e: e.get("pin_order", 0))

        if self.sort_mode == "last_copied":
            unpinned.sort(
                key=lambda e: parse_timestamp(
                    e.get("last_copied_at") or e.get("created_at")
                ),
                reverse=True,
            )
        else:
            unpinned.sort(key=self._calculate_score, reverse=True)

        return (pinned + unpinned)[:limit]