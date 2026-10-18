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
└── AGENTS.md            # This file
```

## Template File Conventions
- `.jinja` suffix → file is rendered with Jinja2
- No `.jinja` suffix → file copied as-is
- `{% if condition %}filename{% endif %}.jinja` → conditional file
- `{{variable}}/` → directory name from user input
- Variables come from `copier.yaml` questions

## Development Workflow

### Package Management
- Use `uv` for all dependency management - never use `pip` directly

### Available Commands
```bash
uv run --locked poe sync           # Sync dependencies
uv run --locked poe setup          # Sync + install hooks
uv run --locked poe format         # Format code with ruff
uv run --locked poe lint           # Lint with ruff
uv run --locked poe check          # Type check with mypy
uv run --locked poe test           # Run template tests
uv run --locked poe flc            # Fix lint + Format + Check
uv run --locked poe flct           # Fix lint + Format + Check + Test
uv run --locked poe validate       # Non-mutating checks + tests
uv run --locked poe generate       # Generate test project to /tmp
```

### Testing Changes
1. **Unit tests**: `uv run --locked poe test` - tests template generation with various options
2. **Manual testing**: `uv run --locked poe generate` - creates project at `/tmp/test-project`

### Code Quality
- `tests/` - checked by ruff and mypy
- `template/` - excluded from linting (contains Jinja templates)
- Run `uv run --locked poe validate` before committing

## Testing Patterns

Tests verify generated projects using `copier.run_copy()` with `unsafe=True` and
`vcs_ref="HEAD"` so the proposed template is tested. The generated package uses
`src/` layout. Use the uv version pinned in `uv.toml`; commit lockfile changes
when updating dependencies.

Run Docker regression tests with
`RUN_DOCKER_TESTS=1 uv run --locked pytest -m docker -v` when changing packaging or
container behavior. These require a running Docker daemon.

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
