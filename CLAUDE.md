# Python Copier Template

This is a **Copier template project**, not a Python application.

## Project Purpose

This repository contains a [Copier](https://copier.readthedocs.io/) template that generates Python projects. When working here, you are:
- Editing **template source files**, not application code
- Writing **Jinja2 templates** that will be rendered into real files
- Testing **template generation**, not application logic

## Project Structure
```
python-template/
├── copier.yaml          # Template configuration & questions
├── template/            # Files that get copied to generated projects
│   ├── *.jinja          # Jinja templates (rendered)
│   └── *                # Static files (copied as-is)
├── tests/               # Tests for template generation
└── CLAUDE.md            # This file
```

## Template File Conventions
- `.jinja` suffix → file is rendered with Jinja2
- No `.jinja` suffix → file copied as-is
- `{% if condition %}filename{% endif %}.jinja` → conditional file
- `{{variable}}/` → directory name from user input
- Variables come from `copier.yaml` questions

## Development Workflow

### Package Management
- Use `uv` for all dependency management — never use `pip` directly

### Available Commands
```bash
uv run poe sync           # Sync dependencies
uv run poe format         # Format code with ruff
uv run poe lint           # Lint with ruff
uv run poe check          # Type check with mypy
uv run poe test           # Run template tests
uv run poe flc            # Format + Lint + Check
uv run poe flct           # Format + Lint + Check + Test
uv run poe generate       # Generate test project to /tmp
```

### Testing Changes
1. **Unit tests**: `uv run poe test` — tests template generation with various options
2. **Manual testing**: `uv run poe generate` — creates project at `/tmp/test-project`

### Code Quality
- `tests/` — checked by ruff and mypy
- `template/` — excluded from linting (contains Jinja templates)
- Run `uv run poe flc` before committing

## Testing Patterns

Tests verify that the Copier template generates valid projects using `copier.run_copy()` with `unsafe=True`.

Key patterns:
- Test all boolean option combinations (enabled/disabled)
- Verify generated files exist and have correct content
- Validate generated projects pass their own linting/tests
- Use `tmp_path` fixture for isolation

## What NOT to Do
- Don't add application logic (APIs, databases, business logic)
- Don't install runtime dependencies in this project
- Don't confuse template tests with generated project tests
- Don't edit files in `template/` without `.jinja` if they need variables
