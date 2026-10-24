# Task runner. Run `uv run just` to list the recipes.

# List the available recipes.
default:
    @just --list

# Run every check CI runs; the gate before any commit.
verify:
    uv run ruff format --check
    uv run ruff check
    uv run mypy
    uv run pytest --cov

# Apply formatting and Ruff's safe fixes.
fix:
    uv run ruff format
    uv run ruff check --fix
