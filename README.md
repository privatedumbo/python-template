# Python Copier Template

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
[![CI - Template Validation](https://github.com/privatedumbo/python-template/actions/workflows/ci.yaml/badge.svg)](https://github.com/privatedumbo/python-template/actions/workflows/ci.yaml)

A [Copier](https://copier.readthedocs.io/) template for modern Python projects. Batteries included with UV, Ruff, Mypy, Pytest, and more.

---

## ✨ Features

### Development Tools

- 📦 **[UV](https://docs.astral.sh/uv/)** - Ultra-fast Python package manager
- 🚀 **[Poe the Poet](https://poethepoet.natn.io/)** - Modern task runner
- 💅 **[Ruff](https://docs.astral.sh/ruff/)** - Lightning-fast linter and formatter
- 🔍 **[Mypy](https://mypy.readthedocs.io/)** - Static type checker
- 🧪 **[Pytest](https://docs.pytest.org/)** - Testing framework with coverage

### Always Included

- 🛫 **Prek hooks** - Automated code quality checks
- 🤖 **AGENTS.md** - Best practices for AI-assisted development

### Optional

- 🐳 **Docker** - Multi-stage builds using uv
- 🔄 **GitHub Actions** - Validation and template-update workflows
- 🐘 **PostgreSQL** - PostgreSQL 18 through Compose, SQLAlchemy, and Alembic migrations

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [Copier](https://copier.readthedocs.io/) (`uv tool install copier`)

### Generate a New Project

```bash
# From GitHub (recommended)
copier copy gh:privatedumbo/python-template my-awesome-project

# From a local clone
copier copy /path/to/python-template my-awesome-project
```

### Interactive Prompts

Copier will ask you a series of questions to customize your project:

| Question | Description | Default |
|----------|-------------|---------|
| `project_slug` | Project/package name (lowercase, underscores) | - |
| `description` | Short project description | "A Python project" |
| `author_name` | Author's full name | - |
| `author_email` | Author's email | - |
| `github_username` | GitHub username/organization | - |
| `python_version` | Minimum Python version and development, CI, and Docker interpreter | 3.14 |
| `license` | Project license | MIT |
| `include_docker` | Include Docker support | Yes |
| `include_github_actions` | Include GitHub Actions workflows | Yes |
| `include_postgres` | Include PostgreSQL 18, SQLAlchemy, and Alembic migrations | No |

Yes/no prompts mark the default selected by Enter with an uppercase letter:
`(Y/n)` for Docker and GitHub Actions, `(y/N)` for PostgreSQL. Both uppercase and
lowercase answers are accepted. Saved answers become the defaults on updates.
The database option is independent of the application Dockerfile option.

### Example

```bash
$ copier copy gh:privatedumbo/python-template my-project

🐍 Python Project Generator
═══════════════════════════════════════════════════════

This template creates a modern Python project with:
• uv for fast dependency management
• Ruff for linting and formatting
• mypy for type checking
• pytest for testing
• prek for commit hooks

Let's configure your new project!

🎤 Project name
   my_project
🎤 Project description
   A library for processing data
🎤 Author name
   John Doe
🎤 Author email
   john@example.com
🎤 GitHub username or organization
   johndoe
🎤 Python version
   3.14 (recommended)
🎤 Project license
   MIT (permissive, simple)
🎤 Include Docker support?
   Yes
🎤 Include GitHub Actions workflows?
   Yes
🎤 Include PostgreSQL and Alembic migrations?
   No
    create  .copier-answers.yml
    create  AGENTS.md
    create  .gitignore
    create  .pre-commit-config.yaml
    create  .python-version
    create  uv.toml
    create  renovate.json
    create  .dockerignore
    create  Dockerfile
    create  LICENSE
    create  README.md
    create  src/my_project/__init__.py
    create  src/my_project/__main__.py
    create  src/my_project/main.py
    create  src/my_project/py.typed
    create  pyproject.toml
    create  scripts/app.toml
    create  tests/__init__.py
    create  tests/test_core.py
    create  .github/workflows/ci.yaml
    create  .github/actions/validation/action.yaml
```

---

## 🔄 Updating Your Project

When this template is updated, you can pull in the changes:

```bash
cd my-awesome-project
copier update
```

Copier will intelligently merge template updates with your local changes.

---

## 🧪 Template Development

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/privatedumbo/python-template.git
cd python-template

# Install dependencies
uv sync --locked
```

### Running Tests

```bash
# Run all tests
uv run --locked poe test

# Validate without changing source or dependency versions
uv run --locked poe validate
```

### Manual Testing

Generate a project to a temporary directory:

```bash
uv run --locked poe generate
```

This creates a test project at `/tmp/test-project`. Use a fresh destination.

The uv version is pinned in `uv.toml`; install it before running repository tasks.
Generated projects keep Python 3.14 as the default and offer 3.13 and 3.15.
Tests validate generated projects on all three interpreters.

```bash
uv run --locked poe validate  # Non-mutating checks and template tests
RUN_DOCKER_TESTS=1 uv run --locked pytest -m docker -v
```

Docker tests build and run generated images, including Python 3.15 and the
no-license option. They also exercise PostgreSQL 18 migrations, data persistence
across down/up, and destruction of the isolated test database. They require a
running Docker daemon with Docker Compose.

Projects generated with PostgreSQL support include `compose.db.yaml`,
`.env.example`, Alembic configuration, and a SQLAlchemy base in the package's
`db.py`. After copying `.env.example` to `.env`, use `poe db:up` to start the
database, `poe db:setup` to apply migrations, `poe db:down` to preserve data while
removing the container, and `poe db:destroy` to remove the container and its data.

Enable the Renovate GitHub App to activate `renovate.json`. The repository config
includes custom extraction for pinned tools inside Jinja templates, while each
generated project receives its own updater configuration. Version pins shared
by uv configuration, dev dependencies, and Docker must be updated together.

Existing generated projects need to merge application modules into `src/` when
updating. See the generated README migration instructions before adopting this
layout change.

---

## 📁 Template Structure

```
python-template/
├── copier.yaml              # Copier configuration & questions
├── template/                # Template source files
│   ├── src/{{project_slug}}/ # Installed package (templated name)
│   │   ├── __init__.py
│   │   ├── __main__.py.jinja
│   │   ├── main.py.jinja
│   │   └── py.typed
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_core.py.jinja
│   ├── scripts/
│   │   └── app.toml.jinja
│   ├── .github/             # GitHub Actions (conditional)
│   ├── AGENTS.md.jinja      # AI agent instructions (always included)
│   ├── pyproject.toml.jinja
│   ├── README.md.jinja
│   ├── Dockerfile.jinja     # Docker support (conditional)
│   └── ...
├── tests/                   # Template tests
│   └── test_template.py
└── pyproject.toml           # Template project config
```

---

## 📝 License

This template is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [Copier](https://github.com/copier-org/copier) - The awesome template engine
- [UV](https://github.com/astral-sh/uv) - Ultra-fast Python package manager
- [Ruff](https://github.com/astral-sh/ruff) - Lightning-fast linter
