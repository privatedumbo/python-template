"""Tests for the Copier template generation."""

import os
import subprocess
import tomllib
from pathlib import Path
from uuid import uuid4

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
        "python_version": "3.14",
        "license": "MIT",
        "include_docker": True,
        "include_github_actions": True,
        "include_postgres": False,
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
        vcs_ref="HEAD",
    )

    # Check core files exist
    assert (tmp_path / "pyproject.toml").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / ".pre-commit-config.yaml").exists()
    assert (tmp_path / "scripts" / "app.toml").exists()
    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / ".editorconfig").exists()

    # Check project structure
    assert (tmp_path / "src" / "test_project").is_dir()
    assert (tmp_path / "src" / "test_project" / "__init__.py").exists()
    assert (tmp_path / "src" / "test_project" / "main.py").exists()
    assert (tmp_path / "tests").is_dir()
    assert (tmp_path / "tests" / "test_core.py").exists()
    assert not (tmp_path / "compose.db.yaml").exists()
    assert not (tmp_path / "alembic.ini").exists()
    assert not (tmp_path / "migrations").exists()
    assert not (tmp_path / ".env.example").exists()
    assert not (tmp_path / "src" / "test_project" / "db.py").exists()
    project = tomllib.loads((tmp_path / "pyproject.toml").read_text())
    assert project["project"]["dependencies"] == []
    tasks = tomllib.loads((tmp_path / "scripts" / "app.toml").read_text())
    assert not any(name.startswith("db:") for name in tasks["tool"]["poe"]["tasks"])


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
        vcs_ref="HEAD",
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
        vcs_ref="HEAD",
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
        vcs_ref="HEAD",
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
        vcs_ref="HEAD",
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
        vcs_ref="HEAD",
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
        vcs_ref="HEAD",
    )

    assert not (tmp_path / ".github").exists()


def test_template_generates_agents_md(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> None:
    """Test that AGENTS.md is always generated."""
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
        vcs_ref="HEAD",
    )

    assert (tmp_path / "AGENTS.md").exists()

    # Verify Python version is templated
    agents_md = (tmp_path / "AGENTS.md").read_text()
    assert "3.14" in agents_md


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
        vcs_ref="HEAD",
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
        vcs_ref="HEAD",
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
        vcs_ref="HEAD",
    )

    answers_file = tmp_path / ".copier-answers.yml"
    assert answers_file.exists()
    content = answers_file.read_text()
    assert "project_slug: test_project" in content


def run_command(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env.pop("UV_PROJECT_ENVIRONMENT", None)
    env["UV_PYTHON"] = (project / ".python-version").read_text().strip()
    return subprocess.run(
        args,
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )


def succeeds(project: Path, *args: str) -> str:
    result = run_command(project, *args)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.fixture
def installed_project(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
) -> Path:
    run_copy(
        str(template_path),
        tmp_path,
        data=default_answers,
        unsafe=True,
        vcs_ref="HEAD",
    )
    succeeds(tmp_path, "uv", "lock")
    succeeds(tmp_path, "uv", "sync", "--locked")
    return tmp_path


@pytest.mark.parametrize("python_version", ["3.13", "3.14", "3.15"])
@pytest.mark.parametrize("include_postgres", [False, True])
def test_generated_project_validation_and_entry_point(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
    python_version: str,
    include_postgres: bool,
) -> None:
    run_copy(
        str(template_path),
        tmp_path,
        data={
            **default_answers,
            "python_version": python_version,
            "include_postgres": include_postgres,
        },
        unsafe=True,
        vcs_ref="HEAD",
    )
    succeeds(tmp_path, "uv", "lock")
    succeeds(tmp_path, "uv", "sync", "--locked")
    before = (tmp_path / "uv.lock").read_bytes()
    succeeds(tmp_path, "uv", "run", "--locked", "poe", "validate")
    output = succeeds(tmp_path, "uv", "run", "--locked", "python", "-m", "test_project")
    assert output.strip() == "Hello from test_project!"
    assert (tmp_path / "uv.lock").read_bytes() == before
    if include_postgres:
        # Revision scaffolding must work and pass checks without a running database.
        succeeds(
            tmp_path, "uv", "run", "--locked", "alembic", "revision", "-m", "Initial"
        )
        succeeds(tmp_path, "uv", "run", "--locked", "poe", "validate")


def test_validation_rejects_bad_code_without_repairing_it(
    installed_project: Path,
) -> None:
    source = installed_project / "src" / "test_project" / "main.py"
    invalid = "import os\n\n" + source.read_text()
    source.write_text(invalid)
    result = run_command(installed_project, "uv", "run", "--locked", "poe", "validate")
    assert result.returncode != 0
    assert "F401" in result.stdout + result.stderr
    assert source.read_text() == invalid

    unformatted = (
        source.read_text()
        .replace("import os\n\n", "")
        .replace(
            'return "Hello from test_project!"',
            "return 'Hello from test_project!'",
        )
    )
    source.write_text(unformatted)
    result = run_command(installed_project, "uv", "run", "--locked", "poe", "validate")
    assert result.returncode != 0
    assert "would be reformatted" in (result.stdout + result.stderr).lower()
    assert source.read_text() == unformatted


def test_mypy_checks_test_code_and_missing_imports(installed_project: Path) -> None:
    test = installed_project / "tests" / "test_bad.py"
    test.write_text('value: int = "wrong"\n')
    result = run_command(installed_project, "uv", "run", "--locked", "poe", "check")
    assert result.returncode != 0
    assert "test_bad.py" in result.stdout
    test.write_text("import nonexistent_template_audit_module\n")
    result = run_command(installed_project, "uv", "run", "--locked", "poe", "check")
    assert result.returncode != 0
    assert "import-not-found" in result.stdout


def test_stale_lockfile_is_rejected(installed_project: Path) -> None:
    lock = (installed_project / "uv.lock").read_bytes()
    project = installed_project / "pyproject.toml"
    project.write_text(
        project.read_text().replace('version = "0.0.1"', 'version = "0.0.2"')
    )
    result = run_command(installed_project, "uv", "sync", "--locked")
    assert result.returncode != 0
    assert (installed_project / "uv.lock").read_bytes() == lock


def test_src_layout_wheel_runs_outside_checkout(installed_project: Path) -> None:
    succeeds(installed_project, "uv", "build")
    wheel = next((installed_project / "dist").glob("*.whl"))
    env_path = installed_project / "wheel-env"
    succeeds(installed_project, "uv", "venv", str(env_path))
    python = env_path / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    succeeds(
        installed_project, "uv", "pip", "install", "--python", str(python), str(wheel)
    )
    result = subprocess.run(
        [str(python), "-I", "-m", "test_project"],
        cwd=env_path,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "Hello from test_project!"


def test_tool_versions_agree(installed_project: Path, template_path: Path) -> None:
    config = tomllib.loads((installed_project / "uv.toml").read_text())
    version = config["required-version"].removeprefix("==")
    project = tomllib.loads((installed_project / "pyproject.toml").read_text())
    assert f"uv=={version}" in project["dependency-groups"]["dev"]
    assert (
        f"ARG UV_VERSION={version}\n" in (installed_project / "Dockerfile").read_text()
    )
    assert (template_path / "uv.toml").read_text() == (
        installed_project / "uv.toml"
    ).read_text()


@pytest.mark.docker
@pytest.mark.skipif(
    os.environ.get("RUN_DOCKER_TESTS") != "1", reason="Set RUN_DOCKER_TESTS=1"
)
@pytest.mark.parametrize(
    ("python_version", "license_name", "include_postgres"),
    [
        ("3.14", "MIT", False),
        ("3.14", "None", False),
        ("3.15", "MIT", False),
        ("3.14", "MIT", True),
    ],
)
def test_generated_docker_runs_as_non_root(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
    license_name: str,
    python_version: str,
    include_postgres: bool,
) -> None:
    run_copy(
        str(template_path),
        tmp_path,
        data={
            **default_answers,
            "license": license_name,
            "python_version": python_version,
            "include_postgres": include_postgres,
        },
        unsafe=True,
        vcs_ref="HEAD",
    )
    succeeds(tmp_path, "uv", "lock")
    image = f"python-template-test:{uuid4().hex}"
    succeeds(tmp_path, "docker", "build", "-t", image, ".")
    try:
        output = succeeds(tmp_path, "docker", "run", "--rm", image)
        assert output.strip() == "Hello from test_project!"
        uid = succeeds(
            tmp_path, "docker", "run", "--rm", "--entrypoint", "id", image, "-u"
        )
        assert uid.strip() == "10001"
        if include_postgres:
            # The runtime image must include the migration environment and driver.
            succeeds(
                tmp_path,
                "docker",
                "run",
                "--rm",
                "--env",
                "DATABASE_URL=postgresql+psycopg://app@localhost/app",
                image,
                "alembic",
                "upgrade",
                "head",
                "--sql",
            )
    finally:
        succeeds(tmp_path, "docker", "image", "rm", image)


@pytest.mark.parametrize("include_docker", [False, True])
def test_postgres_is_independent_of_application_docker(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
    include_docker: bool,
) -> None:
    run_copy(
        str(template_path),
        tmp_path,
        data={
            **default_answers,
            "include_postgres": True,
            "include_docker": include_docker,
        },
        unsafe=True,
        vcs_ref="HEAD",
    )
    assert (tmp_path / "Dockerfile").exists() == include_docker
    assert (tmp_path / "compose.db.yaml").exists()
    assert (tmp_path / ".env.example").exists()
    assert (tmp_path / "migrations" / "versions").is_dir()
    assert (tmp_path / "alembic.ini").exists()
    tasks = tomllib.loads((tmp_path / "scripts" / "app.toml").read_text())
    assert {"db:up", "db:down", "db:destroy", "db:setup"} <= tasks["tool"]["poe"][
        "tasks"
    ].keys()


@pytest.mark.docker
@pytest.mark.skipif(
    os.environ.get("RUN_DOCKER_TESTS") != "1", reason="Set RUN_DOCKER_TESTS=1"
)
def test_postgres_migrations_and_lifecycle(
    template_path: Path,
    default_answers: dict[str, str | bool],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Keep all resources isolated, even when run alongside a developer's databases.
    for key in (
        "DATABASE_URL",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "COMPOSE_PROJECT_NAME",
    ):
        monkeypatch.delenv(key, raising=False)
    run_copy(
        str(template_path),
        tmp_path,
        data={**default_answers, "include_postgres": True, "include_docker": False},
        unsafe=True,
        vcs_ref="HEAD",
    )
    succeeds(tmp_path, "uv", "lock")
    succeeds(tmp_path, "uv", "sync", "--locked")
    compose_name = f"template-db-{uuid4().hex}"
    env_file = tmp_path / ".env"
    env_file.write_text(
        (tmp_path / ".env.example")
        .read_text()
        .replace("POSTGRES_PORT=5432", "POSTGRES_PORT=0")
        + f"\nCOMPOSE_PROJECT_NAME={compose_name}\n"
    )
    uv = ("uv", "run", "--locked")
    with_env = (*uv, "--env-file", ".env")
    compose = ("docker", "compose", "--env-file", ".env", "-f", "compose.db.yaml")

    def sql(statement: str) -> str:
        code = (
            "from sqlalchemy import create_engine, text\n"
            "from test_project.db import get_database_url\n"
            "with create_engine(get_database_url()).begin() as connection:\n"
            f"    result = connection.execute(text({statement!r}))\n"
            "    print(result.scalar() if result.returns_rows else 'ok')\n"
        )
        return succeeds(tmp_path, *with_env, "python", "-c", code).strip()

    try:
        succeeds(tmp_path, *uv, "poe", "db:up")
        address = succeeds(tmp_path, *compose, "port", "postgres", "5432").strip()
        port = address.rsplit(":", 1)[1]
        env_file.write_text(
            env_file.read_text().replace("POSTGRES_PORT=0", f"POSTGRES_PORT={port}")
        )
        assert sql("SHOW server_version").startswith("18.")
        # An empty migration directory must also support initial setup.
        succeeds(tmp_path, *uv, "poe", "db:setup")

        source = tmp_path / "src" / "test_project" / "db.py"
        source.write_text(
            source.read_text().replace(
                "from sqlalchemy.orm import DeclarativeBase",
                "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column",
            )
            + "\n\nclass Example(Base):\n"
            + '    __tablename__ = "example"\n'
            + "    id: Mapped[int] = mapped_column(primary_key=True)\n"
        )
        succeeds(
            tmp_path,
            *with_env,
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            "Add example",
        )
        revisions = list((tmp_path / "migrations" / "versions").glob("*.py"))
        assert len(revisions) == 1
        assert "op.create_table(" in revisions[0].read_text()
        succeeds(tmp_path, *uv, "poe", "validate")
        succeeds(tmp_path, *uv, "poe", "db:setup")
        succeeds(tmp_path, *uv, "poe", "db:setup")
        succeeds(tmp_path, *with_env, "alembic", "check")
        sql("INSERT INTO example (id) VALUES (42)")
        succeeds(tmp_path, *uv, "poe", "db:down")
        succeeds(tmp_path, *uv, "poe", "db:up")
        assert sql("SELECT id FROM example") == "42"
        succeeds(tmp_path, *with_env, "alembic", "downgrade", "base")
        assert sql("SELECT to_regclass('public.example')") == "None"
        succeeds(tmp_path, *uv, "poe", "db:setup")
        sql("INSERT INTO example (id) VALUES (43)")
        succeeds(tmp_path, *uv, "poe", "db:destroy")
        succeeds(tmp_path, *uv, "poe", "db:up")
        assert sql("SELECT to_regclass('public.example')") == "None"
        succeeds(tmp_path, *uv, "poe", "db:setup")
        assert sql("SELECT count(*) FROM example") == "0"
    finally:
        succeeds(tmp_path, *uv, "poe", "db:destroy")
