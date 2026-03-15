"""Tests for the Task dataclass."""

import pytest
from src.task import Task, Priority, Status


class TestTask:
    """Test cases for Task dataclass."""

    def test_create_task_with_defaults(self):
        """Test creating a task with minimal required fields."""
        task = Task(id=1, title="Test task")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.description is None
        assert task.due_date is None
        assert task.priority == Priority.MEDIUM
        assert task.status == Status.TODO
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields specified."""
        task = Task(
            id=1,
            title="Full task",
            description="A complete task",
            due_date="2026-12-31",
            priority=Priority.HIGH,
            status=Status.TODO,
        )

        assert task.id == 1
        assert task.title == "Full task"
        assert task.description == "A complete task"
        assert task.due_date == "2026-12-31"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO

    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            id=1,
            title="Test task",
            description="Description",
            priority=Priority.LOW,
        )
        result = task.to_dict()

        assert result["id"] == 1
        assert result["title"] == "Test task"
        assert result["description"] == "Description"
        assert result["priority"] == "low"
        assert result["status"] == "todo"

    def test_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            "id": 1,
            "title": "From dict",
            "description": "Test description",
            "due_date": "2026-06-15",
            "priority": "high",
            "status": "done",
            "created_at": "2026-01-01T10:00:00",
            "updated_at": "2026-01-01T10:00:00",
        }
        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "From dict"
        assert task.priority == Priority.HIGH
        assert task.status == Status.DONE

    def test_mark_done(self):
        """Test marking a task as done."""
        task = Task(id=1, title="Test")
        original_updated = task.updated_at

        task.mark_done()

        assert task.status == Status.DONE
        assert task.updated_at >= original_updated

    def test_mark_todo(self):
        """Test marking a task as todo."""
        task = Task(id=1, title="Test", status=Status.DONE)

        task.mark_todo()

        assert task.status == Status.TODO
