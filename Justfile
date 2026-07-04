# ==========================================
# Global Settings
# ==========================================

set dotenv-load := true

TARGETS := "src tests"
HOOK_TYPES := "pre-commit pre-push"

# ==========================================
# Default Task
# ==========================================

default:
    @just --list

# ==========================================
# ALL
# ==========================================

all: prepare-hooks modify verify

# ==========================================
# Git Hook
# ==========================================

prepare-hooks:
    @for hook in {{HOOK_TYPES}}; do \
        echo "Installing hook: $hook ..."; \
        uv run pre-commit install --hook-type $hook; \
    done

# ==========================================
# Modification
# ==========================================

modify: ruff-modify

ruff-modify:
    uv run ruff check --fix {{TARGETS}}
    uv run ruff format {{TARGETS}}

# ==========================================
# Verification
# ==========================================

verify: ruff-verify type test

ruff-verify:
    uv run ruff check {{TARGETS}}
    uv run ruff format --check {{TARGETS}}

type:
    uv run mypy {{TARGETS}}

test:
    uv run pytest
