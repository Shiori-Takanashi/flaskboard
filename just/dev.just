# just/dev.just

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

# ==========================================
# Git Hook
# ==========================================

HOOK_TYPES := "pre-commit pre-push"

hooks:
    @for hook in {{HOOK_TYPES}}; do \
        echo "Installing hook: $hook ..."; \
        uv run pre-commit install --hook-type $hook; \
    done
