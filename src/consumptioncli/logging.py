import json
import logging
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, override


class StructuredFormatter(logging.Formatter):
    @override
    def format(self, record: logging.LogRecord) -> str:
        log: Mapping[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "data"):
            log["data"] = record.__dict__["data"]

        return json.dumps(log, default=str)


def setup_logging(log_path: Path):
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Backend Logging
    backend_handler = logging.FileHandler(log_path)
    backend_handler.setFormatter(StructuredFormatter())

    backend_logger = logging.getLogger("consumptionbackend")
    backend_logger.setLevel(logging.INFO)
    backend_logger.addHandler(backend_handler)
