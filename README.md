# Task Manager

A CLI task management tool for personal productivity, built using the Ralph Wiggum autonomous development technique.

## Lab 7 Submission

**Repository:** https://github.com/zaya-8900/task-manager

### Requirements Checklist

| Requirement | Status |
|-------------|--------|
| GitHub repository with Task Manager | ✅ |
| PROMPT.md file | ✅ |
| SPEC.md file | ✅ |
| IMPLEMENTATION_PLAN.md file | ✅ |
| Phase 1: Project structure | ✅ |
| Phase 1: Task dataclass | ✅ |
| Phase 1: Storage utilities | ✅ |
| Phase 2: `task add` command | ✅ |
| Phase 2: `task list` command | ✅ |
| Phase 2: `task done` command | ✅ |
| Phase 3: Additional commands | ✅ |
| Tests passing | ✅ (37 tests) |

## Installation

```bash
pip install click pytest
```

## Usage

```bash
# Add a task
python -m src.cli add "Buy groceries" --description "Milk, eggs" --due 2026-03-20 --priority high

# List all tasks
python -m src.cli list

# Filter by status or priority
python -m src.cli list --status todo
python -m src.cli list --priority high

# Mark task as done
python -m src.cli done 1

# Edit a task
python -m src.cli edit 1 --title "New title" --priority low

# Search tasks
python -m src.cli search "groceries"

# Delete a task
python -m src.cli delete 1
```

## Project Structure

```
task-manager/
├── PROMPT.md              # Ralph Wiggum iteration instructions
├── SPEC.md                # Project specification
├── IMPLEMENTATION_PLAN.md # Development checklist
├── README.md              # This file
├── pyproject.toml         # Python project configuration
├── src/
│   ├── __init__.py
│   ├── task.py            # Task dataclass with Priority/Status enums
│   ├── storage.py         # JSON persistence utilities
│   └── cli.py             # Click-based CLI commands
└── tests/
    ├── __init__.py
    ├── test_task.py       # Task dataclass tests
    ├── test_storage.py    # Storage utility tests
    └── test_cli.py        # CLI command tests
```

## Running Tests

```bash
pytest tests/ -v
```

## Progress

- **Phase 1:** ✅ Complete - Project setup, Task dataclass, storage utilities
- **Phase 2:** ✅ Complete - Core commands (add, list, done)
- **Phase 3:** ✅ Complete - Additional commands (delete, edit, search)
- **Phase 4:** ⏳ Pending - Polish (error handling, colored output)
