import os
import json


class Config:
    def __init__(self, config_file: str = "data/config.json"):
        self.config_file = config_file
        self.data = self._load()

    def _load(self) -> dict:
        if not os.path.exists(self.config_file):
            return {}
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def get(self, key: str, default=None):
        return self.data.get(key, default)