"""Workflow engine for Flowwork."""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, List, Optional

from .models import CarePlan, Patient, Stage, Task
from .reporting import build_patient_summary


class FlowworkEngine:
    """Handle patient progression through an oncology care plan."""

    def __init__(self, care_plan: CarePlan, storage) -> None:
        self.care_plan = care_plan
        self.storage = storage

    def register_patient(self, identifier: str, full_name: str, age: int) -> Patient:
        if self.storage.get(identifier):
            raise ValueError(f"Le patient {identifier} existe déjà")
        patient = Patient(
            identifier=identifier,
            full_name=full_name,
            age=age,
            diagnosis=self.care_plan.diagnosis,
        )
        self._initialise_task_status(patient)
        self.storage.save(patient)
        return patient

    def _initialise_task_status(self, patient: Patient) -> None:
        stage = self.current_stage(patient)
        for task in stage.tasks:
            patient.task_status[self._task_key(stage, task)] = "todo"

    def current_stage(self, patient: Patient) -> Stage:
        try:
            return self.care_plan.stages[patient.current_stage_index]
        except IndexError as exc:
            raise ValueError("Le patient est hors du plan de soins") from exc

    def list_patients(self) -> Iterable[Patient]:
        yield from self.storage.all()

    def get_patient(self, identifier: str) -> Optional[Patient]:
        return self.storage.get(identifier)

    def complete_task(self, identifier: str, task_name: str) -> Patient:
        patient = self._require_patient(identifier)
        stage = self.current_stage(patient)
        task = self._find_task(stage, task_name)
        key = self._task_key(stage, task)
        patient.task_status[key] = "done"
        if self._stage_completed(stage, patient):
            self._advance_stage(patient)
        self.storage.save(patient)
        return patient

    def _stage_completed(self, stage: Stage, patient: Patient) -> bool:
        return all(
            patient.task_status.get(self._task_key(stage, task)) == "done"
            for task in stage.tasks
        )

    def _advance_stage(self, patient: Patient) -> None:
        patient.current_stage_index += 1
        if patient.current_stage_index < len(self.care_plan.stages):
            next_stage = self.care_plan.stages[patient.current_stage_index]
            for task in next_stage.tasks:
                patient.task_status[self._task_key(next_stage, task)] = "todo"

    def _find_task(self, stage: Stage, task_name: str) -> Task:
        for task in stage.tasks:
            if task.name.lower() == task_name.lower():
                return task
        raise ValueError(f"Tâche '{task_name}' introuvable dans l'étape {stage.name}")

    def _task_key(self, stage: Stage, task: Task) -> str:
        return f"{stage.name}::{task.name}"

    def _require_patient(self, identifier: str) -> Patient:
        patient = self.get_patient(identifier)
        if not patient:
            raise ValueError(f"Patient {identifier} introuvable")
        return patient

    def patient_summary(self, identifier: str) -> Dict[str, object]:
        patient = self._require_patient(identifier)
        return build_patient_summary(self.care_plan, patient)

    def export_patient(self, identifier: str) -> Dict[str, object]:
        patient = self._require_patient(identifier)
        return asdict(patient)

