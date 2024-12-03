# log_entry.py
from datetime import datetime
from typing import Dict, Optional

class LogEntry:
    def __init__(self, timestamp: datetime, level: str, message: str, metrics: Optional[Dict[str, float]] = None):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.metrics = metrics or {}

    def __repr__(self):
        return f"LogEntry({self.timestamp}, {self.level}, {self.message})"
