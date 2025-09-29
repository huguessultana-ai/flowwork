"""Reporting helpers for Flowwork."""

from __future__ import annotations

from typing import Dict, List

from .models import CarePlan, Patient, Stage, Task


def build_patient_summary(care_plan: CarePlan, patient: Patient) -> Dict[str, object]:
    """Return a dict summarising the patient's progress."""

    stages_summary: List[Dict[str, object]] = []
    for index, stage in enumerate(care_plan.stages):
        stages_summary.append(
            {
                "stage": stage.name,
                "objectives": stage.objectives,
                "status": _stage_status(stage, patient, index),
                "tasks": [
                    {
                        "name": task.name,
                        "description": task.description,
                        "status": patient.task_status.get(_task_key(stage, task), "todo"),
                        "due_in_days": task.due_in_days,
                    }
                    for task in stage.tasks
                ],
            }
        )

    return {
        "identifier": patient.identifier,
        "full_name": patient.full_name,
        "diagnosis": patient.diagnosis,
        "current_stage": _current_stage_name(care_plan, patient),
        "stages": stages_summary,
    }


def _stage_status(stage: Stage, patient: Patient, index: int) -> str:
    if patient.current_stage_index == index:
        return "en cours"
    keys = [_task_key(stage, task) for task in stage.tasks]
    if all(patient.task_status.get(key) == "done" for key in keys):
        return "terminé"
    if any(patient.task_status.get(key) == "done" for key in keys):
        return "partiel"
    return "à faire"


def _task_key(stage: Stage, task: Task) -> str:
    return f"{stage.name}::{task.name}"


def _current_stage_name(care_plan: CarePlan, patient: Patient) -> str:
    if patient.current_stage_index >= len(care_plan.stages):
        return "Plan terminé"
    return care_plan.stages[patient.current_stage_index].name

