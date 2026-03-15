"""JSON storage utilities for task persistence."""

import json
from pathlib import Path
from typing import Optional

from .task import Task


DEFAULT_STORAGE_PATH = Path.home() / ".task-manager" / "tasks.json"


class Storage:
    """Handles reading and writing tasks to JSON file.

    Attributes:
        path: Path to the JSON storage file.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        """Initialize storage with optional custom path.

        Args:
            path: Custom path for the JSON file. Uses default if not provided.
        """
        self.path = path or DEFAULT_STORAGE_PATH
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Create storage directory and file if they don't exist."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write_data({"tasks": []})

    def _read_data(self) -> dict:
        """Read raw data from JSON file."""
        with open(self.path, "r") as f:
            return json.load(f)

    def _write_data(self, data: dict) -> None:
        """Write raw data to JSON file."""
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self) -> list[Task]:
        """Load all tasks from storage.

        Returns:
            List of Task objects.
        """
        data = self._read_data()
        return [Task.from_dict(t) for t in data.get("tasks", [])]

    def save_tasks(self, tasks: list[Task]) -> None:
        """Save all tasks to storage.

        Args:
            tasks: List of Task objects to save.
        """
        data = {"tasks": [t.to_dict() for t in tasks]}
        self._write_data(data)

    def add_task(self, task: Task) -> None:
        """Add a single task to storage.

        Args:
            task: Task to add.
        """
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def get_next_id(self) -> int:
        """Get the next available task ID.

        Returns:
            Next available ID (max existing ID + 1, or 1 if no tasks).
        """
        tasks = self.load_tasks()
        if not tasks:
            return 1
        return max(t.id for t in tasks) + 1

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The ID of the task to find.

        Returns:
            The Task if found, None otherwise.
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task: Task) -> bool:
        """Update an existing task.

        Args:
            task: Task with updated values.

        Returns:
            True if task was found and updated, False otherwise.
        """
        tasks = self.load_tasks()
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                self.save_tasks(tasks)
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: ID of task to delete.

        Returns:
            True if task was found and deleted, False otherwise.
        """
        tasks = self.load_tasks()
        original_count = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]
        if len(tasks) < original_count:
            self.save_tasks(tasks)
            return True
        return False
