import json
import os
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE_DIR = ROOT / "sample_data"
DEFAULT_AUDIT_LOG = ROOT / "demo_runtime" / "audit_log.jsonl"


class DataStore:
    def __init__(self, sample_dir: Optional[Path] = None, audit_log: Optional[Path] = None):
        self.sample_dir = sample_dir or Path(os.getenv("SAMPLE_DATA_DIR", DEFAULT_SAMPLE_DIR))
        if not self.sample_dir.is_absolute():
            self.sample_dir = ROOT / self.sample_dir
        self.audit_log = audit_log or Path(os.getenv("COPILOT_AUDIT_LOG", DEFAULT_AUDIT_LOG))
        if not self.audit_log.is_absolute():
            self.audit_log = ROOT / self.audit_log
        self.audit_log.parent.mkdir(parents=True, exist_ok=True)

    def load_json(self, name: str) -> Any:
        with (self.sample_dir / name).open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def trips(self) -> list[dict[str, Any]]:
        return self.load_json("trips.json")

    def drivers(self) -> list[dict[str, Any]]:
        return self.load_json("drivers.json")

    def passengers(self) -> list[dict[str, Any]]:
        return self.load_json("passengers.json")

    def dispatch_events(self) -> list[dict[str, Any]]:
        return self.load_json("dispatch_events.json")

    def risk_events(self) -> list[dict[str, Any]]:
        return self.load_json("risk_events.json")

    def certification_summary(self) -> dict[str, Any]:
        return self.load_json("certification_summary.json")

    def get_trip(self, order_id: str) -> Optional[dict[str, Any]]:
        return next((trip for trip in self.trips() if trip["order_id"] == order_id), None)

    def get_driver(self, driver_id: Optional[str]) -> Optional[dict[str, Any]]:
        if not driver_id:
            return None
        return next((driver for driver in self.drivers() if driver["driver_id"] == driver_id), None)

    def get_passenger(self, passenger_id: Optional[str]) -> Optional[dict[str, Any]]:
        if not passenger_id:
            return None
        return next((passenger for passenger in self.passengers() if passenger["passenger_id"] == passenger_id), None)

    def events_for_order(self, order_id: str) -> dict[str, list[dict[str, Any]]]:
        return {
            "dispatch": [event for event in self.dispatch_events() if event["order_id"] == order_id],
            "risk": [event for event in self.risk_events() if event["order_id"] == order_id],
        }

    def append_audit(self, record: dict[str, Any]) -> None:
        with self.audit_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    def read_audit(self) -> list[dict[str, Any]]:
        if not self.audit_log.exists():
            return []
        records: list[dict[str, Any]] = []
        with self.audit_log.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
