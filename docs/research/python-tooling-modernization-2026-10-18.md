# Python template modernization assessment

Research date: 2026-10-18. Repository inspected at `381cc4a`. This is a recommendation document, not an implementation. Findings combine local source inspection, experiments on a temporary generated project, official documentation, and upstream project configurations. Live branch links can change after this date. No comparative performance benchmarks were run.

The template already has a sound stack. Keep uv, Ruff, pytest, Poe, Copier, and initially Hatchling. Adopt prek if you want the newer hook runner. Keep strict mypy as the general-purpose default while evaluating ty on real applications. The highest-value modernization is making generation, validation, upgrades, and container execution reliable.

| Area | Decision | Reason |
| --- | --- | --- |
| uv | Keep; tighten version and lockfile handling | Existing dependency groups and project workflow are appropriate |
| Hooks | Prefer prek; retain YAML and split the combined hook | Practical environment-management improvements without changing the workflow |
| Types | Keep mypy default; trial ty intentionally | Beta status alone is not disqualifying, but annotation policy and framework behavior differ |
| Ruff | Keep; explicit fixes and reviewed rule selection | Current configuration lets upgrades introduce policy changes and CI edit files |
| Tests | Keep pytest; add strict configuration and artifact tests | Test the output users install and run |
| CI/CD | Keep GitHub Actions; repair validation and automate updates | Enforced checks and tested releases matter more than newer action labels |
| Docker | Keep the multi-stage design; repair and smoke-test it | Current default output fails to build and launch |
| Hatchling/Poe | Keep | No demonstrated problem requiring replacement |

**Observed behavior in a newly generated project**

Generated from local `HEAD`, selecting Python 3.14, MIT, Docker, and GitHub Actions. Local uv was 0.11.2; generated execution used CPython 3.14.3. Initial `uv sync --all-extras` succeeded and freshly resolved Ruff 0.17.1, mypy 2.4.0, pytest 9.1.1, and pytest-cov 7.1.0. These are observed resolutions, not a recommended permanent version set.

| Check | Result | Implication |
| --- | --- | --- |
| Generated pytest | 1 passed; 75% line coverage | The example function works, but the test does not validate the entry point |
| Generated mypy over package and tests | Passed, four source files | The initial typed example is valid |
| Generated `poe flct` | Failed on four `CPY001` copyright-notice diagnostics | Fresh generations already break with the newly resolved Ruff rules |
| `ruff check --select F401` after adding an unused import to the temporary project | Fixed the file and exited 0 without CLI `--fix` | Global `fix = true` makes nominal validation mutate code |
| Original generated Docker build | Failed: `Readme file does not exist: README.md` | Docker omits metadata required by the declared build backend |
| Build after copying README and LICENSE into the temporary build stage | Passed | Confirms the immediate packaging blocker |
| Run that image | Failed: `No module named audit_project.__main__` | Generated `CMD` does not match the generated package |
| Inspect image runtime user | Empty configured user | Dockerfile does not explicitly select a non-root runtime user |

Only the temporary generated specimen was adjusted during reproduction. The repository's implementation files were not changed. The full template test suite, Python 3.15 compatibility, and a complete proposed replacement Dockerfile were not tested.

**Python version policy**

Python 3.15.0 was released on October 9, 2026. Add a 3.15 compatibility lane and offer it once generated projects and their dependencies pass. Keeping 3.14 as a conservative application default during that validation is reasonable; do not label it the newest release. Separate the minimum supported version, developer interpreter, and deployment interpreter conceptually. Libraries should test their minimum and latest supported interpreter; applications should always test their deployed interpreter. [Python 3.15 release](https://www.python.org/downloads/release/python-3150/).

Currently the template defaults to 3.14, but generated-project CI and `default_answers` select only 3.13. Root `requires-python >=3.12`, root `.python-version` 3.13, and its CI matrix also need an intentional support policy. A matrix entry is not sufficient if uv selects a pinned interpreter instead: configure `setup-uv`'s `python-version` or `UV_PYTHON` explicitly. Keeping `setup-python` alongside uv is supported, though uv can manage Python itself. [uv GitHub Actions integration](https://docs.astral.sh/uv/guides/integration/github/).

**uv and packaging**

Keep `[dependency-groups]`, a committed `uv.lock`, and `uv sync`/`uv run`. A generated project must first resolve its own lockfile, then commit it. Do not copy this template repository's lockfile into generated projects. Use `uv sync --locked` in ordinary CI; `--locked` rejects stale locks whereas `--frozen` skips freshness validation. The root workflow currently uses unlocked sync. The generated composite already uses locked sync, which is worth retaining. After deliberate synchronization, use locked execution or `--no-sync` consistently. [uv locking semantics](https://docs.astral.sh/uv/concepts/projects/sync/).

Choose and record a tested uv version for CI and Docker. The setup action's version and the installed uv version are separate choices. Document the tested developer version too. Stop using `pip install copier` in the update workflow; invoke a controlled Copier version through uv.

Add one dependency updater, not two. For ordinary generated GitHub projects, Dependabot supports the `uv` ecosystem and lockfile updates; also configure GitHub Actions and optional Docker updates. Renovate is attractive if you want broader coordinated configuration and custom maintenance of `.jinja` sources. Normal ecosystem discovery should not be assumed to update template files containing Jinja. Include fresh-generation checks so changing a minimum tool version is tested against real output. [uv/Dependabot](https://docs.astral.sh/uv/guides/integration/dependabot/), [uv/Renovate](https://docs.astral.sh/uv/guides/integration/renovate/).

Do not install every optional extra in production by default. The current Docker `--all-extras` is harmless with no extras, but becomes an inappropriate deployment policy as projects grow. Select required runtime extras explicitly. If splitting dev into lint/test/docs groups later, use `--no-default-groups` for production rather than assuming `--no-dev` removes every development group. A single dev group is sufficient today. [uv group and extra semantics](https://docs.astral.sh/uv/concepts/projects/sync/).

Keep Hatchling initially. `uv_build` is a credible optional simplification for pure-Python packages and defaults to a `src/` package layout. It currently does not build extension modules; custom build hooks/layouts can justify Hatchling. If adopting it, follow its documented bounded backend requirement rather than an unbounded dependency. Build backend replacement does not fix missing metadata files or entry points. [uv build backend](https://docs.astral.sh/uv/concepts/build-backend/).

Modernize package license metadata to an SPDX string and explicit license files, mapping the template's GPL choice to the intended valid SPDX identifier. Preserve the conditional no-license case. This is a small standards update with clear packaging value. [PyPA pyproject guidance](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).

**Hooks and Ruff**

Pre-commit is still a valid workflow. Prek offers a compatible runner with uv-backed Python environments, sharing of environments/toolchains, and native implementations of supported common hooks. I recommend switching the runner while retaining `.pre-commit-config.yaml` initially. Replace installation with `uv run prek install` and validate all hooks once. This recommendation is based on operational design and adoption, not a measured speedup in this repository. [prek documentation](https://prek.j178.dev/), [compatibility differences](https://prek.j178.dev/compatibility/).

Specific migration trap: prek discovers nested configurations, including this repository's `template/.pre-commit-config.yaml`. Exclude that nested project through root `.prekignore` or deliberate single-config invocation. Discovery exclusions and exclusions from ancestor hooks are distinct; configure both as needed. [prek workspaces](https://prek.j178.dev/reference/workspace/).

Replace the single whole-project `flc` hook with separate Ruff fix, Ruff format, and type-check hooks. Pass changed filenames to Ruff, using `--force-exclude`; run type checking over the project with `pass_filenames: false`. Trigger type checks for relevant configuration and lockfile changes too. Keep project-local tool execution so hooks and CI use the same locked tools. Run lint fixes before formatting because fixes can produce code needing reformatting. [Ruff integrations](https://docs.astral.sh/ruff/integrations/).

Remove global `fix = true`; fixes should be explicit in developer commands. CI needs a separate read-only validation task. Current generated `flct` formats and fixes before testing, while root `ruff check .` also inherits automatic fixing. Neither is a reliable check of committed lint/format state.

Revisit `select = ["ALL"]`. It opts into newly added rules on upgrade, which the fresh-generation failure demonstrates. Prefer an explicit set of rule families matching your policies, or keep ALL only with controlled upgrades and review of newly enabled rules. Do not suppress actual correctness problems just to make an upgrade pass. With no generated lock initially, deliberately bound fast-changing dev-tool releases or otherwise maintain tested constraints; existing projects still need reviewed lockfile updates. [Ruff rule selection](https://docs.astral.sh/ruff/linter/).

**mypy versus ty**

Ty's current README still declares beta status and allows breaking diagnostic/API changes between 0.0.x versions. Astral's December 2025 announcement nevertheless recommends it to motivated production users. This makes it suitable for a deliberate trial, not automatically unsuitable until a GA label appears. [ty project status](https://github.com/astral-sh/ty), [Astral beta announcement](https://astral.sh/blog/ty).

My recommendation is to retain strict mypy as this broad template's default, and offer ty as an intentional choice for new applications after checking their real dependencies. Ty does not enforce missing annotations or load mypy plugins. It now has built-in Pydantic support; claiming Pydantic is wholly unsupported would be stale. Framework behavior still requires verification. [ty typing FAQ](https://docs.astral.sh/ty/reference/typing-faq/).

Your template ignores Ruff's `ANN` rules because mypy enforces annotations. Replacing only the checker command would silently remove that policy. A ty option should restore annotation rules and explicitly configure appropriate strictness diagnostics, including missing generic parameters and unsound return statements. Review suppressions rather than mechanically copying mypy codes. [ty migration guide](https://docs.astral.sh/ty/coming-from-mypy-or-pyright/).

For mypy, remove global `ignore_missing_imports = true`, install available stubs, and scope unavoidable exceptions to specific dependencies. Missing imports otherwise introduce Any and weaken strict checking. Include tests in the generated type-check task if typed tests are the desired policy; currently the task checks only the package. [mypy common issues](https://mypy.readthedocs.io/en/stable/common_issues.html).

Evaluate ty on a representative application briefly alongside mypy. Check intentional failures as well as clean runs: wrong return values, missing annotations, unresolved imports, decorators, and framework constructors. Lock the version and review updates. Choose one long-term checker once evidence supports that decision; permanent dual checking need not be the default for every application.

**Testing**

Keep pytest, pytest-cov, parametrization, `tmp_path`, and actual Copier generation. Add `testpaths = ["tests"]`, pytest 9 `strict = true`, and `--import-mode=importlib`. Strict settings catch configuration/marker mistakes and unexpected successful xfails; lock upgrades because strict mode can expand. The existing pyproject configuration table is fine. [pytest strict settings](https://docs.pytest.org/en/stable/reference/reference.html#confval-strict).

Prefer `src/{{ project_slug }}/` for new installable projects, together with importlib test imports. The purpose is to reduce accidental imports from the checkout and make installed-package behavior visible. Still add an isolated wheel-install test outside the checkout; src layout alone does not prove distributions are complete. Existing projects should migrate layout separately from unrelated tooling changes. [pytest integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html).

Use branch coverage, retain meaningful exclusions through `exclude_also`, and express `skip_covered` as a TOML boolean. Separate quick local tests from explicit coverage runs if coverage becomes a feedback cost. Establish a project-specific coverage floor only after covering important behavior; the passing hello test with a broken container is evidence that percentages alone are insufficient. [coverage configuration](https://coverage.readthedocs.io/en/latest/config.html).

Template-specific acceptance checks should include:

1. Render every offered Python version and every Docker/Actions Boolean combination; parse TOML/YAML and cover all license choices.
2. Test the default Python choice through generated install, non-mutating validation, and tests.
3. Build sdist and wheel, install the built wheel in an isolated environment, and run import/entry-point checks outside the checkout. For libraries, exercise the suite against that artifact. [uv build guidance](https://docs.astral.sh/uv/guides/package/).
4. Build and launch the default Docker image, assert its expected output/exit status and runtime user.
5. Make Copier tests explicitly use `vcs_ref="HEAD"` and CLI `--vcs-ref=HEAD`. Otherwise adding release tags can cause tests to select the latest tag instead of the proposed template. No local tags were present during inspection, so this is a latent risk. [Copier revision selection implementation](https://github.com/copier-org/copier/blob/master/copier/_cli.py).
6. Add an old-generation-to-new-template update scenario before distributing disruptive layout or tooling changes.

Do not add tox/nox, Hypothesis, xdist, async plugins, or Testcontainers as mandatory template dependencies without a need. uv, Poe, and the GitHub matrix already cover the simple workflow. Add those tools when compatibility orchestration, meaningful property tests, test duration, async code, or external services justify them.

**CI/CD**

The standard validation sequence should synchronize the lockfile without changing it, then run non-mutating Ruff checks, the chosen type checker, and tests. Separate fast checks from compatibility jobs when duplication becomes material. Add default-branch push validation, timeouts, and cancellation of superseded PR jobs.

Use read-only permissions for CI, immutable action SHA pins with readable version comments, and disable persisted checkout credentials when unused. Pair pins with automated maintenance. Review current action releases and runner requirements during implementation rather than just replacing major numbers. Move the update workflow's `version` input into an environment variable instead of interpolating it into executable shell. [GitHub secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

The template-update workflow has a separate correctness gap: PRs created with its default `GITHUB_TOKEN` do not trigger ordinary push/pull_request workflows. Adding push alone does not fix that suppression. Validate the resulting update within the workflow; use a narrowly scoped GitHub App token if the usual PR checks must trigger automatically. [create-pull-request token documentation](https://github.com/peter-evans/create-pull-request#token).

The current optional Actions output is CI plus template updates, not application deployment. Keep CD opt-in. For publishable libraries, build and test artifacts once, then publish those exact files from a separate protected job using PyPI Trusted Publishing and job-scoped `id-token: write`. For applications, deployment should follow the actual platform and promote the image already tested, without rebuilding a different artifact. [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/).

**Docker**

Keep multi-stage builds, BuildKit cache mounts, `UV_LINK_MODE=copy`, optional bytecode compilation, and non-editable production installation. They are useful design choices. Update the implementation as follows:

1. Copy README and any declared license/build metadata before the final installation.
2. Provide a real `__main__.py` or console entry point, or run the existing `<package>.main` module consistently.
3. Explicitly create/select a non-root user. `COPY --chown` changes ownership; it does not set the runtime identity.
4. Derive both stages from the same pinned Python base and copy in a separately versioned uv binary. The two floating tags observed during this audit resolved independently, so matching their label text is not a strong reproducibility guarantee.
5. Validate lock freshness at the final sync. A deliberate frozen dependency-only layer can remain useful when full project metadata is not yet available.
6. Install only required runtime dependencies and extras; copy the installed environment plus required runtime assets into the final image.
7. Add `.dockerignore` for environments, Git data, caches, and local secrets, especially before broadening source copies. Prefer `COPY` for ordinary files.
8. Make build-and-run smoke testing part of template CI.

These recommendations follow [uv's Docker guidance](https://docs.astral.sh/uv/guides/integration/docker/) and [Docker's build guidance](https://docs.docker.com/build/building/best-practices/). Keep a slim Debian base unless measurements or deployment requirements justify Alpine or distroless. An HTTP health check belongs in a service-specific template, not a generic Python hello-world image.

**What established projects demonstrate**

| Project | Observed practice | Relevant lesson |
| --- | --- | --- |
| FastAPI | uv groups, prek, separate hooks, both mypy and ty | Modern maintainers can adopt ty gradually while retaining mypy. [Config](https://github.com/fastapi/fastapi/blob/master/pyproject.toml), [lint script](https://github.com/fastapi/fastapi/blob/master/scripts/lint.sh), [hooks](https://github.com/fastapi/fastapi/blob/master/.pre-commit-config.yaml) |
| Pydantic | uv, pytest strictness, artifact testing, SHA pins, pre-commit | Reliability improvements coexist with established tools. [CI](https://github.com/pydantic/pydantic/blob/main/.github/workflows/ci.yml), [config](https://github.com/pydantic/pydantic/blob/main/pyproject.toml) |
| HTTPX | Hatchling, strict mypy, focused Ruff selection, pytest | A good project need not replace every tool with its newest alternative. Its older CI version matrix is not a recommendation here. [Config](https://github.com/encode/httpx/blob/master/pyproject.toml) |
| Astral uv Docker example | Cached installation stages and explicit runtime packaging | Copy the maintained architecture, then test this template's own entry point and build inputs. [Example](https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile) |

**Suggested implementation order**

1. Repair fresh-generation Ruff compatibility, Docker metadata and entry point, and mutating CI; add regression checks at the generated-project boundary.
2. Make lock/version handling deliberate, test the actual default and artifacts, and repair template-update PR validation.
3. Adopt prek, split hooks, improve mypy configuration, and enable pytest strict/importlib defaults.
4. Add automated maintenance and evaluate Python 3.15; consider src layout with an explicit Copier-update migration check.
5. Trial ty on a representative new application. Revisit the template default after framework and annotation-policy validation.

No change to the default build backend, task runner, container distribution, or release process is required merely to appear current.
