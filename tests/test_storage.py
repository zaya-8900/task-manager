"""Tests for storage utilities."""

import pytest
import tempfile
from pathlib import Path

from src.task import Task, Priority, Status
from src.storage import Storage


@pytest.fixture
def temp_storage():
    """Create a temporary storage file for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test_tasks.json"
        yield Storage(path)


class TestStorage:
    """Test cases for Storage class."""

    def test_storage_creates_file(self, temp_storage):
        """Test that storage creates file on initialization."""
        assert temp_storage.path.exists()

    def test_load_empty_tasks(self, temp_storage):
        """Test loading tasks from empty storage."""
        tasks = temp_storage.load_tasks()
        assert tasks == []

    def test_add_and_load_task(self, temp_storage):
        """Test adding and loading a task."""
        task = Task(id=1, title="Test task")
        temp_storage.add_task(task)

        tasks = temp_storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test task"

    def test_get_next_id_empty(self, temp_storage):
        """Test getting next ID when no tasks exist."""
        next_id = temp_storage.get_next_id()
        assert next_id == 1

    def test_get_next_id_with_tasks(self, temp_storage):
        """Test getting next ID with existing tasks."""
        temp_storage.add_task(Task(id=1, title="Task 1"))
        temp_storage.add_task(Task(id=2, title="Task 2"))

        next_id = temp_storage.get_next_id()
        assert next_id == 3

    def test_get_task_by_id_found(self, temp_storage):
        """Test getting a task by ID when it exists."""
        temp_storage.add_task(Task(id=1, title="Find me"))

        task = temp_storage.get_task_by_id(1)
        assert task is not None
        assert task.title == "Find me"

    def test_get_task_by_id_not_found(self, temp_storage):
        """Test getting a task by ID when it doesn't exist."""
        task = temp_storage.get_task_by_id(999)
        assert task is None

    def test_update_task(self, temp_storage):
        """Test updating an existing task."""
        task = Task(id=1, title="Original")
        temp_storage.add_task(task)

        task.title = "Updated"
        result = temp_storage.update_task(task)

        assert result is True
        loaded = temp_storage.get_task_by_id(1)
        assert loaded.title == "Updated"

    def test_update_task_not_found(self, temp_storage):
        """Test updating a non-existent task."""
        task = Task(id=999, title="Ghost")
        result = temp_storage.update_task(task)
        assert result is False

    def test_delete_task(self, temp_storage):
        """Test deleting a task."""
        temp_storage.add_task(Task(id=1, title="Delete me"))

        result = temp_storage.delete_task(1)

        assert result is True
        assert temp_storage.get_task_by_id(1) is None

    def test_delete_task_not_found(self, temp_storage):
        """Test deleting a non-existent task."""
        result = temp_storage.delete_task(999)
        assert result is False

    def test_save_multiple_tasks(self, temp_storage):
        """Test saving multiple tasks at once."""
        tasks = [
            Task(id=1, title="Task 1", priority=Priority.HIGH),
            Task(id=2, title="Task 2", priority=Priority.LOW),
        ]
        temp_storage.save_tasks(tasks)

        loaded = temp_storage.load_tasks()
        assert len(loaded) == 2
        assert loaded[0].priority == Priority.HIGH
        assert loaded[1].priority == Priority.LOW
