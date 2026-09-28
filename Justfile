# ==========================================
# Global Settings
# ==========================================

# `dev/gunicorn`ブランチでは不要。
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

modify: ruff-modify djl-modify djh-modify

ruff-modify:
    uv run ruff check --fix {{TARGETS}}
    uv run ruff format {{TARGETS}}

djl-modify:
    uv run djlint --reformat {{TARGETS}}

djh-modify:
    uv run djhtml {{TARGETS}}

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

djl-verify:
    uv run djlint --lint {{TARGETS}}


# ==========================================
# Flask Migrate
# ==========================================

db-init:
    docker container exec flaskboard-app flask db init

db-migrate:
    docker container exec flaskboard-app flask db migrate

db-upgrade:
    docker container exec flaskboard-app flask db upgrade
