def compact_pin_order(history: list[dict]) -> None:
    pinned = [e for e in history if e.get("pinned")]
    pinned.sort(key=lambda e: e.get("pin_order", 0))

    for idx, entry in enumerate(pinned):
        entry["pin_order"] = idx