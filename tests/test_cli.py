"""Tests for CLI commands."""

import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner

from src.cli import main
from src.storage import Storage
from src.task import Task, Priority, Status


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_storage(monkeypatch):
    """Create a temporary storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test_tasks.json"
        storage = Storage(path)
        # Monkeypatch the storage in cli module
        import src.cli
        monkeypatch.setattr(src.cli, "storage", storage)
        yield storage


class TestAddCommand:
    """Tests for the add command."""

    def test_add_basic_task(self, runner, temp_storage):
        """Test adding a task with just a title."""
        result = runner.invoke(main, ["add", "Buy milk"])

        assert result.exit_code == 0
        assert "Added task 1: Buy milk" in result.output

        tasks = temp_storage.load_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy milk"

    def test_add_task_with_description(self, runner, temp_storage):
        """Test adding a task with description."""
        result = runner.invoke(main, ["add", "Shopping", "-d", "Get groceries"])

        assert result.exit_code == 0
        tasks = temp_storage.load_tasks()
        assert tasks[0].description == "Get groceries"

    def test_add_task_with_due_date(self, runner, temp_storage):
        """Test adding a task with due date."""
        result = runner.invoke(main, ["add", "Report", "--due", "2026-12-31"])

        assert result.exit_code == 0
        tasks = temp_storage.load_tasks()
        assert tasks[0].due_date == "2026-12-31"

    def test_add_task_with_priority(self, runner, temp_storage):
        """Test adding a task with priority."""
        result = runner.invoke(main, ["add", "Urgent", "-p", "high"])

        assert result.exit_code == 0
        tasks = temp_storage.load_tasks()
        assert tasks[0].priority == Priority.HIGH

    def test_add_task_invalid_due_date(self, runner, temp_storage):
        """Test adding a task with invalid due date."""
        result = runner.invoke(main, ["add", "Task", "--due", "invalid"])

        assert result.exit_code == 1
        assert "Error" in result.output


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty(self, runner, temp_storage):
        """Test listing when no tasks exist."""
        result = runner.invoke(main, ["list"])

        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_list_all_tasks(self, runner, temp_storage):
        """Test listing all tasks."""
        temp_storage.add_task(Task(id=1, title="Task 1"))
        temp_storage.add_task(Task(id=2, title="Task 2"))

        result = runner.invoke(main, ["list"])

        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" in result.output

    def test_list_filter_by_status(self, runner, temp_storage):
        """Test filtering tasks by status."""
        temp_storage.add_task(Task(id=1, title="Todo task", status=Status.TODO))
        temp_storage.add_task(Task(id=2, title="Done task", status=Status.DONE))

        result = runner.invoke(main, ["list", "-s", "done"])

        assert result.exit_code == 0
        assert "Done task" in result.output
        assert "Todo task" not in result.output

    def test_list_filter_by_priority(self, runner, temp_storage):
        """Test filtering tasks by priority."""
        temp_storage.add_task(Task(id=1, title="High", priority=Priority.HIGH))
        temp_storage.add_task(Task(id=2, title="Low", priority=Priority.LOW))

        result = runner.invoke(main, ["list", "-p", "high"])

        assert result.exit_code == 0
        assert "High" in result.output
        assert "Low" not in result.output


class TestDoneCommand:
    """Tests for the done command."""

    def test_mark_task_done(self, runner, temp_storage):
        """Test marking a task as done."""
        temp_storage.add_task(Task(id=1, title="Complete me"))

        result = runner.invoke(main, ["done", "1"])

        assert result.exit_code == 0
        assert "Marked task 1 as done" in result.output

        task = temp_storage.get_task_by_id(1)
        assert task.status == Status.DONE

    def test_done_nonexistent_task(self, runner, temp_storage):
        """Test marking a non-existent task as done."""
        result = runner.invoke(main, ["done", "999"])

        assert result.exit_code == 1
        assert "not found" in result.output


class TestDeleteCommand:
    """Tests for the delete command."""

    def test_delete_task(self, runner, temp_storage):
        """Test deleting a task."""
        temp_storage.add_task(Task(id=1, title="Delete me"))

        result = runner.invoke(main, ["delete", "1"])

        assert result.exit_code == 0
        assert "Deleted task 1" in result.output
        assert temp_storage.get_task_by_id(1) is None

    def test_delete_nonexistent_task(self, runner, temp_storage):
        """Test deleting a non-existent task."""
        result = runner.invoke(main, ["delete", "999"])

        assert result.exit_code == 1
        assert "not found" in result.output


class TestEditCommand:
    """Tests for the edit command."""

    def test_edit_title(self, runner, temp_storage):
        """Test editing a task's title."""
        temp_storage.add_task(Task(id=1, title="Original"))

        result = runner.invoke(main, ["edit", "1", "-t", "Updated"])

        assert result.exit_code == 0
        task = temp_storage.get_task_by_id(1)
        assert task.title == "Updated"

    def test_edit_priority(self, runner, temp_storage):
        """Test editing a task's priority."""
        temp_storage.add_task(Task(id=1, title="Task", priority=Priority.LOW))

        result = runner.invoke(main, ["edit", "1", "-p", "high"])

        assert result.exit_code == 0
        task = temp_storage.get_task_by_id(1)
        assert task.priority == Priority.HIGH

    def test_edit_nonexistent_task(self, runner, temp_storage):
        """Test editing a non-existent task."""
        result = runner.invoke(main, ["edit", "999", "-t", "New title"])

        assert result.exit_code == 1
        assert "not found" in result.output


class TestSearchCommand:
    """Tests for the search command."""

    def test_search_by_title(self, runner, temp_storage):
        """Test searching tasks by title."""
        temp_storage.add_task(Task(id=1, title="Buy groceries"))
        temp_storage.add_task(Task(id=2, title="Call mom"))

        result = runner.invoke(main, ["search", "groceries"])

        assert result.exit_code == 0
        assert "Buy groceries" in result.output
        assert "Call mom" not in result.output

    def test_search_by_description(self, runner, temp_storage):
        """Test searching tasks by description."""
        temp_storage.add_task(Task(id=1, title="Shopping", description="Buy milk and eggs"))

        result = runner.invoke(main, ["search", "milk"])

        assert result.exit_code == 0
        assert "Shopping" in result.output

    def test_search_no_results(self, runner, temp_storage):
        """Test search with no matching results."""
        temp_storage.add_task(Task(id=1, title="Task"))

        result = runner.invoke(main, ["search", "xyz"])

        assert result.exit_code == 0
        assert "No tasks found" in result.output
