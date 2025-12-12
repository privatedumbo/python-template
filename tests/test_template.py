"""Tests for the Copier template generation."""

import subprocess
from pathlib import Path

import pytest
from copier import run_copy


@pytest.fixture
def template_path() -> Path:
    """Return the path to the template root."""
    return Path(__file__).parent.parent


@pytest.fixture
def default_answers() -> dict[str, str | bool]:
    """Return default answers for template questions."""
    return {
        "project_slug": "test_project",
        "description": "A test project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "github_username": "testuser",
        "python_version": "3.12",
        "license": "MIT",
        "include_docker": True,
        "include_github_actions": True,
        "include_cursor_rules": False,
    }


def test_template_generates_successfully(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that the template generates a valid project structure."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    # Check core files exist
    assert (tmp_path / "pyproject.toml").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / ".pre-commit-config.yaml").exists()
    assert (tmp_path / "scripts" / "app.toml").exists()

    # Check project structure
    assert (tmp_path / "test_project").is_dir()
    assert (tmp_path / "test_project" / "__init__.py").exists()
    assert (tmp_path / "test_project" / "main.py").exists()
    assert (tmp_path / "tests").is_dir()
    assert (tmp_path / "tests" / "test_core.py").exists()


def test_template_generates_correct_project_name(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that project name is correctly templated."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    pyproject = (tmp_path / "pyproject.toml").read_text()
    assert 'name = "test_project"' in pyproject

    readme = (tmp_path / "README.md").read_text()
    # _project_name is derived from project_slug: "test_project" -> "Test Project"
    assert "# Test Project" in readme


def test_template_generates_project_urls(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that project URLs are generated correctly."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    pyproject = (tmp_path / "pyproject.toml").read_text()
    assert "[project.urls]" in pyproject
    assert 'Homepage = "https://github.com/testuser/test_project"' in pyproject
    assert 'Repository = "https://github.com/testuser/test_project"' in pyproject
    assert 'Issues = "https://github.com/testuser/test_project/issues"' in pyproject


def test_template_generates_docker_when_enabled(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that Docker files are generated when include_docker is True."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    assert (tmp_path / "Dockerfile").exists()
    dockerfile = (tmp_path / "Dockerfile").read_text()
    assert "test_project" in dockerfile


def test_template_skips_docker_when_disabled(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that Docker files are not generated when include_docker is False."""
    answers = {**default_answers, "include_docker": False}
    run_copy(
        str(template_path),
        tmp_path,
        data=answers,
        unsafe=True,
    )

    assert not (tmp_path / "Dockerfile").exists()


def test_template_generates_github_actions_when_enabled(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that GitHub Actions are generated when include_github_actions is True."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    assert (tmp_path / ".github" / "workflows" / "ci.yaml").exists()
    assert (tmp_path / ".github" / "actions" / "validation" / "action.yaml").exists()


def test_template_skips_github_actions_when_disabled(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that GitHub Actions are not generated when disabled."""
    answers = {**default_answers, "include_github_actions": False}
    run_copy(
        str(template_path),
        tmp_path,
        data=answers,
        unsafe=True,
    )

    assert not (tmp_path / ".github").exists()


def test_template_generates_cursor_rules_when_enabled(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that Cursor rules are generated when include_cursor_rules is True."""
    answers = {**default_answers, "include_cursor_rules": True}
    run_copy(
        str(template_path),
        tmp_path,
        data=answers,
        unsafe=True,
    )

    assert (tmp_path / ".cursor" / "rules").is_dir()
    assert (tmp_path / ".cursor" / "rules" / "python.mdc").exists()
    assert (tmp_path / ".cursor" / "rules" / "development.mdc").exists()
    assert (tmp_path / ".cursor" / "rules" / "testing.mdc").exists()
    assert (tmp_path / ".cursor" / "rules" / "database.mdc").exists()

    # Verify Python version is templated
    python_rules = (tmp_path / ".cursor" / "rules" / "python.mdc").read_text()
    assert "Python 3.12" in python_rules


def test_template_skips_cursor_rules_when_disabled(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that Cursor rules are not generated when disabled."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    assert not (tmp_path / ".cursor").exists()


def test_template_generates_license_mit(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that MIT license is generated correctly."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    license_file = tmp_path / "LICENSE"
    assert license_file.exists()
    license_content = license_file.read_text()
    assert "MIT License" in license_content
    assert "Test Author" in license_content


def test_template_skips_license_when_none(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that no license file is generated when license is None."""
    answers = {**default_answers, "license": "None"}
    run_copy(
        str(template_path),
        tmp_path,
        data=answers,
        unsafe=True,
    )

    assert not (tmp_path / "LICENSE").exists()

    # Also verify license field is not in pyproject.toml
    pyproject = (tmp_path / "pyproject.toml").read_text()
    assert "license" not in pyproject.lower() or "license =" not in pyproject


def test_template_generates_copier_answers_file(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that .copier-answers.yml is generated."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    answers_file = tmp_path / ".copier-answers.yml"
    assert answers_file.exists()
    content = answers_file.read_text()
    assert "project_slug: test_project" in content


def test_generated_project_passes_validation(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that the generated project passes linting, formatting, and type checking."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    # Initialize uv and sync dependencies
    result = subprocess.run(
        ["uv", "sync", "--all-extras"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"uv sync failed: {result.stderr}"

    # Run format check
    result = subprocess.run(
        ["uv", "run", "ruff", "format", "--check", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"ruff format check failed: {result.stdout}"

    # Run lint check
    result = subprocess.run(
        ["uv", "run", "ruff", "check", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"ruff lint failed: {result.stdout}"

    # Run type check with mypy
    result = subprocess.run(
        ["uv", "run", "mypy", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"mypy failed: {result.stdout}\n{result.stderr}"


def test_generated_project_tests_pass(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that the generated project's tests pass."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
    )

    # Sync dependencies
    subprocess.run(
        ["uv", "sync", "--all-extras"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )

    # Run pytest
    result = subprocess.run(
        ["uv", "run", "pytest", str(tmp_path / "tests"), "-v"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"pytest failed: {result.stdout}\n{result.stderr}"
