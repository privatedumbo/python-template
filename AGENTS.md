# Agent Instructions

## Working with Rules

- **Suggest rule additions proactively**
  - If you notice a repeated pattern, preference, or guideline that could be formalized
  - If a request seems like it should be part of the project's standards
  - **Do not add rules without asking** - only suggest and explain where it would fit
  - Let the user decide whether to add it and make the changes themselves

## General Coding Principles

### SOLID Principles
Follow SOLID principles in all code:
- **Single Responsibility**: Each function/class should have one clear purpose
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for their base types
- **Interface Segregation**: Prefer small, focused interfaces over large ones
- **Dependency Inversion**: Depend on abstractions, not concrete implementations

### Code Organization
- **Prefer functions over classes** when possible
  - Use functions for simple, stateless operations
  - Only introduce classes when you need state management or complex behavior
  - Favor composition over inheritance

- **Avoid global variables**
  - Pass dependencies explicitly through function parameters
  - Use dependency injection patterns when needed
  - Keep state localized and controlled

- **Configuration management**
  - Use `pydantic-settings` for application configuration
  - Define settings as Pydantic models with proper validation
  - Load from environment variables when appropriate
  - Keep configuration immutable after initialization

- **Data models**
  - Use `dataclasses` for internal domain models (lightweight, no validation overhead)
  - Use `Pydantic` models for external boundaries (APIs, user input, file parsing)
  - Validate at system boundaries, trust internal data

## Best Practices
- Write small, focused functions that do one thing well
- Keep functions pure when possible (no side effects)
- Make dependencies explicit through parameters
- Use type hints to make contracts clear
