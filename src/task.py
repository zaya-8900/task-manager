"""Task dataclass for the task manager."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    """Task status options."""
    TODO = "todo"
    DONE = "done"


@dataclass
class Task:
    """Represents a single task in the task manager.

    Attributes:
        id: Unique identifier for the task.
        title: The task title.
        description: Optional detailed description.
        due_date: Optional due date string (YYYY-MM-DD).
        priority: Task priority level.
        status: Current task status.
        created_at: Timestamp when task was created.
        updated_at: Timestamp when task was last updated.
    """
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            due_date=data.get("due_date"),
            priority=Priority(data.get("priority", "medium")),
            status=Status(data.get("status", "todo")),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
        )

    def mark_done(self) -> None:
        """Mark the task as done."""
        self.status = Status.DONE
        self.updated_at = datetime.now().isoformat()

    def mark_todo(self) -> None:
        """Mark the task as todo."""
        self.status = Status.TODO
        self.updated_at = datetime.now().isoformat()
