"""CLI interface for the task manager using Click."""

import click
from datetime import datetime
from typing import Optional

from .task import Task, Priority, Status
from .storage import Storage


# Initialize storage
storage = Storage()


@click.group()
def main():
    """Task Manager - A CLI tool for personal productivity."""
    pass


@main.command()
@click.argument("title")
@click.option("--description", "-d", help="Task description")
@click.option("--due", help="Due date (YYYY-MM-DD)")
@click.option(
    "--priority", "-p",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    default="medium",
    help="Task priority"
)
def add(title: str, description: Optional[str], due: Optional[str], priority: str):
    """Add a new task.

    TITLE is the task title (required).
    """
    # Validate due date if provided
    if due:
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            click.echo("Error: Due date must be in YYYY-MM-DD format", err=True)
            raise SystemExit(1)

    task = Task(
        id=storage.get_next_id(),
        title=title,
        description=description,
        due_date=due,
        priority=Priority(priority.lower()),
    )
    storage.add_task(task)
    click.echo(f"Added task {task.id}: {task.title}")


@main.command("list")
@click.option(
    "--status", "-s",
    type=click.Choice(["done", "todo"], case_sensitive=False),
    help="Filter by status"
)
@click.option(
    "--priority", "-p",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    help="Filter by priority"
)
def list_tasks(status: Optional[str], priority: Optional[str]):
    """List all tasks with optional filters."""
    tasks = storage.load_tasks()

    # Apply filters
    if status:
        tasks = [t for t in tasks if t.status.value == status.lower()]
    if priority:
        tasks = [t for t in tasks if t.priority.value == priority.lower()]

    if not tasks:
        click.echo("No tasks found.")
        return

    # Display tasks
    for task in tasks:
        status_mark = "[x]" if task.status == Status.DONE else "[ ]"
        priority_str = f"({task.priority.value})" if task.priority != Priority.MEDIUM else ""
        due_str = f" due: {task.due_date}" if task.due_date else ""
        click.echo(f"{task.id}. {status_mark} {task.title} {priority_str}{due_str}")


@main.command()
@click.argument("task_id", type=int)
def done(task_id: int):
    """Mark a task as complete.

    TASK_ID is the ID of the task to mark done.
    """
    task = storage.get_task_by_id(task_id)
    if not task:
        click.echo(f"Error: Task {task_id} not found", err=True)
        raise SystemExit(1)

    task.mark_done()
    storage.update_task(task)
    click.echo(f"Marked task {task_id} as done: {task.title}")


@main.command()
@click.argument("task_id", type=int)
def delete(task_id: int):
    """Delete a task.

    TASK_ID is the ID of the task to delete.
    """
    task = storage.get_task_by_id(task_id)
    if not task:
        click.echo(f"Error: Task {task_id} not found", err=True)
        raise SystemExit(1)

    storage.delete_task(task_id)
    click.echo(f"Deleted task {task_id}: {task.title}")


@main.command()
@click.argument("task_id", type=int)
@click.option("--title", "-t", help="New title")
@click.option("--description", "-d", help="New description")
@click.option("--due", help="New due date (YYYY-MM-DD)")
@click.option(
    "--priority", "-p",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    help="New priority"
)
def edit(task_id: int, title: Optional[str], description: Optional[str],
         due: Optional[str], priority: Optional[str]):
    """Edit an existing task.

    TASK_ID is the ID of the task to edit.
    """
    task = storage.get_task_by_id(task_id)
    if not task:
        click.echo(f"Error: Task {task_id} not found", err=True)
        raise SystemExit(1)

    # Validate due date if provided
    if due:
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            click.echo("Error: Due date must be in YYYY-MM-DD format", err=True)
            raise SystemExit(1)

    # Update fields if provided
    if title:
        task.title = title
    if description:
        task.description = description
    if due:
        task.due_date = due
    if priority:
        task.priority = Priority(priority.lower())

    task.updated_at = datetime.now().isoformat()
    storage.update_task(task)
    click.echo(f"Updated task {task_id}: {task.title}")


@main.command()
@click.argument("keyword")
def search(keyword: str):
    """Search tasks by keyword.

    KEYWORD is the search term to look for in titles and descriptions.
    """
    tasks = storage.load_tasks()
    keyword_lower = keyword.lower()

    matches = []
    for task in tasks:
        if keyword_lower in task.title.lower():
            matches.append(task)
        elif task.description and keyword_lower in task.description.lower():
            matches.append(task)

    if not matches:
        click.echo(f"No tasks found matching '{keyword}'")
        return

    click.echo(f"Found {len(matches)} task(s) matching '{keyword}':")
    for task in matches:
        status_mark = "[x]" if task.status == Status.DONE else "[ ]"
        click.echo(f"{task.id}. {status_mark} {task.title}")


if __name__ == "__main__":
    main()
