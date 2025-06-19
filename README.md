# Python Template

My python projects template. Trying to keep it lean.

---

## 🎯 Core Features

### Development Tools

- 📦 UV - Ultra-fast Python package manager
- 🚀 Poe the Poet - Modern command runner with powerful features
- 💅 Ruff - Lightning-fast linter and formatter
- 🔍 Mypy - Static type checker
- 🧪 Pytest - Testing framework with fixtures and plugins

### Infrastructure

- 🛫 Pre-commit hooks
- 🐳 Docker support with multi-stage builds and distroless images
- 🔄 GitHub Actions CI/CD pipeline


## Usage

The template is based on [UV](https://docs.astral.sh/) as package manager. You need to have it installed in your system to use this template.

Once you have that, you can just run:

```bash
$ uv run poe sync
```

to create a virtual environment and install all the dependencies, including the development ones.

You also need to install the pre-commit hooks with:

```bash
$ uv run poe install-hooks
```

### Formatting, Linting and Testing

Format your code:

```bash
$ uv run poe format
```

Run linters (ruff):

```bash
$ uv run poe lint
```

Run type checks (mypy):

```bash
$ uv run poe check
```

Run tests:

```bash
$ uv run poe test
```

Do all of the above:

```bash
$ uv run poe flc  # Format, Lint and Check
$ uv run poe flct # Format, Lint, Check and Test
```

### Docker

The template includes a multi stage Dockerfile, which produces an image with the code and the dependencies installed. You can build the image with:

```bash
$ uv run poe dockerize
```

### Github Actions

The template a Github Action Workflow that runs tests and linters on every push on the main and dev branches. You can find the workflow file in `.github/workflows/main-list-test.yml`.
