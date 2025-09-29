"""Domain models for the Flowwork oncology application."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Task:
    """A clinical task to be performed during a stage."""

    name: str
    description: str
    status: str = "todo"
    due_in_days: Optional[int] = None

    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.status = "done"

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Task":
        return cls(
            name=str(data["name"]),
            description=str(data["description"]),
            status=str(data.get("status", "todo")),
            due_in_days=data.get("due_in_days"),
        )


@dataclass
class Stage:
    """A stage in the oncology care plan."""

    name: str
    objectives: str
    tasks: List[Task] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "objectives": self.objectives,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Stage":
        tasks_data = data.get("tasks", [])
        return cls(
            name=str(data["name"]),
            objectives=str(data.get("objectives", "")),
            tasks=[Task.from_dict(task) for task in tasks_data],
        )


@dataclass
class CarePlan:
    """The full oncology care plan with its stages."""

    diagnosis: str
    stages: List[Stage]

    def to_dict(self) -> Dict[str, object]:
        return {
            "diagnosis": self.diagnosis,
            "stages": [stage.to_dict() for stage in self.stages],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "CarePlan":
        return cls(
            diagnosis=str(data["diagnosis"]),
            stages=[Stage.from_dict(stage) for stage in data.get("stages", [])],
        )


@dataclass
class Patient:
    """Information tracked for a patient in the workflow."""

    identifier: str
    full_name: str
    age: int
    diagnosis: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    current_stage_index: int = 0
    task_status: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        return {
            "identifier": self.identifier,
            "full_name": self.full_name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "created_at": self.created_at.isoformat(),
            "current_stage_index": self.current_stage_index,
            "task_status": self.task_status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Patient":
        created_at_raw = data.get("created_at")
        created_at = (
            datetime.fromisoformat(created_at_raw)
            if isinstance(created_at_raw, str)
            else datetime.utcnow()
        )
        return cls(
            identifier=str(data["identifier"]),
            full_name=str(data["full_name"]),
            age=int(data["age"]),
            diagnosis=str(data["diagnosis"]),
            created_at=created_at,
            current_stage_index=int(data.get("current_stage_index", 0)),
            task_status={str(k): str(v) for k, v in data.get("task_status", {}).items()},
        )

