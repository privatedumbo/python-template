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

### Infrastructure (Optional)

- 🛫 **Pre-commit hooks** - Automated code quality checks
- 🐳 **Docker** - Multi-stage builds with distroless images
- 🔄 **GitHub Actions** - CI/CD pipeline

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Copier](https://copier.readthedocs.io/) (`pipx install copier` or `uv tool install copier`)

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
| `project_name` | Human-readable project name | - |
| `project_slug` | Python package name (lowercase, underscores) | Derived from project_name |
| `description` | Short project description | "A Python project" |
| `author_name` | Author's full name | - |
| `author_email` | Author's email | - |
| `github_username` | GitHub username/organization | - |
| `python_version` | Minimum Python version | 3.12 |
| `license` | Project license | MIT |
| `include_docker` | Include Docker support | Yes |
| `include_github_actions` | Include GitHub Actions CI/CD | Yes |

### Example

```bash
$ copier copy gh:privatedumbo/python-template my-project

🎤 What is your project name?
   My Awesome Project
🎤 Python package name (lowercase, underscores)
   my_awesome_project
🎤 Short description of your project
   A truly awesome Python project
🎤 Author's full name
   John Doe
🎤 Author's email address
   john@example.com
🎤 GitHub username or organization
   johndoe
🎤 Minimum Python version
   3.12
🎤 Project license
   MIT
🎤 Include Docker support?
   Yes
🎤 Include GitHub Actions CI/CD?
   Yes

    create  .
    create  .copier-answers.yml
    create  .gitignore
    create  .pre-commit-config.yaml
    create  .python-version
    create  Dockerfile
    create  LICENSE
    create  README.md
    create  my_awesome_project/__init__.py
    create  my_awesome_project/main.py
    create  pyproject.toml
    create  scripts/app.toml
    create  tests/__init__.py
    create  tests/test_core.py
    ...
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
uv sync --all-extras
```

### Running Tests

```bash
# Run all tests
uv run poe test

# Run full validation (format, lint, check, test)
uv run poe flct
```

### Manual Testing

Generate a project to a temporary directory:

```bash
uv run poe generate
```

This creates a test project at `/tmp/test-project`.

---

## 📁 Template Structure

```
python-template/
├── copier.yaml              # Copier configuration & questions
├── template/                # Template source files
│   ├── {{project_slug}}/    # Package directory (templated name)
│   │   ├── __init__.py
│   │   └── main.py.jinja
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_core.py.jinja
│   ├── scripts/
│   │   └── app.toml.jinja
│   ├── .github/             # GitHub Actions (conditional)
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
