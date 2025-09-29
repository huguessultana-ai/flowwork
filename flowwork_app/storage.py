"""Persistence layer for Flowwork."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, Optional

from .models import Patient


class JsonStorage:
    """Simple JSON file storage for patient records."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({})

    def _write(self, data: Dict[str, Dict[str, object]]) -> None:
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _read(self) -> Dict[str, Dict[str, object]]:
        raw = self.path.read_text() if self.path.exists() else "{}"
        return json.loads(raw) if raw.strip() else {}

    def all(self) -> Iterable[Patient]:
        data = self._read()
        for item in data.values():
            yield Patient.from_dict(item)

    def get(self, identifier: str) -> Optional[Patient]:
        data = self._read()
        item = data.get(identifier)
        return Patient.from_dict(item) if item else None

    def save(self, patient: Patient) -> None:
        data = self._read()
        data[patient.identifier] = patient.to_dict()
        self._write(data)

    def delete(self, identifier: str) -> None:
        data = self._read()
        if identifier in data:
            del data[identifier]
            self._write(data)

