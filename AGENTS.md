# Agent Instructions

This is a **Copier template project**, not a Python application.

## Project Purpose

This repository contains a [Copier](https://copier.readthedocs.io/) template that generates Python projects. When working here, you are:
- Editing **template source files**, not application code
- Writing **Jinja2 templates** that will be rendered into real files
- Testing **template generation**, not application logic

## Key Concepts

### Template Structure
```
python-template/
├── copier.yaml          # Template configuration & questions
├── template/            # Files that get copied to generated projects
│   ├── *.jinja          # Jinja templates (rendered)
│   └── *                # Static files (copied as-is)
├── tests/               # Tests for template generation
└── .cursor/rules/       # Rules for THIS project (not copied)
```

### File Naming Conventions
- `file.py.jinja` → Rendered to `file.py` in generated project
- `{% if condition %}file{% endif %}.jinja` → Conditionally included
- `{{variable}}/` → Directory name from user input

## Working with Templates

### Jinja Syntax
- Use `{{ variable }}` for variable substitution
- Use `{% if condition %}...{% endif %}` for conditionals
- Use `{%- ... -%}` to strip whitespace
- Variables come from `copier.yaml` questions

### Testing Changes
```bash
uv run poe test              # Run all template tests
uv run poe generate          # Generate test project to /tmp
```

### Common Patterns
```jinja
{# Conditional content #}
{% if include_feature %}
feature-specific content
{% endif %}

{# Derived values #}
{{ project_slug | replace('_', '-') }}
```

## What NOT to Do

- ❌ Don't add application logic (APIs, databases, business logic)
- ❌ Don't install runtime dependencies in this project
- ❌ Don't confuse template tests with generated project tests
- ❌ Don't edit files in `template/` without `.jinja` if they need variables
