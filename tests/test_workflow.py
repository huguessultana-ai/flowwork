"""Tests for the Flowwork oncology application."""

from __future__ import annotations

from pathlib import Path

import pytest

from flowwork_app import JsonStorage, default_oncology_plan, FlowworkEngine


def make_engine(tmp_path: Path) -> FlowworkEngine:
    storage = JsonStorage(tmp_path / "patients.json")
    return FlowworkEngine(default_oncology_plan(), storage)


def test_register_and_progress(tmp_path: Path) -> None:
    engine = make_engine(tmp_path)
    patient = engine.register_patient("P001", "Alice Martin", 54)

    summary = engine.patient_summary("P001")
    assert summary["current_stage"] == "Triage initiale"

    engine.complete_task("P001", "Anamnèse infirmière")
    engine.complete_task("P001", "Examens biologiques")

    summary = engine.patient_summary("P001")
    assert summary["current_stage"] == "Diagnostic"

    engine.complete_task("P001", "Biopsie")
    engine.complete_task("P001", "Imagerie")
    engine.complete_task("P001", "RCP")

    summary = engine.patient_summary("P001")
    assert summary["current_stage"] == "Traitement"


def test_cannot_register_duplicate(tmp_path: Path) -> None:
    engine = make_engine(tmp_path)
    engine.register_patient("P002", "Bob Dupont", 67)

    with pytest.raises(ValueError):
        engine.register_patient("P002", "Bob Dupont", 67)

