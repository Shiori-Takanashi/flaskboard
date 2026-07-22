
# Justfile

# ==========================================
# Global Settings
# ==========================================


set shell := ["bash", "-euo", "pipefail", "-c"]

import 'just/dev.just'

TARGETS := "src tests"


# ==========================================
# Default Task
# ==========================================

default:
    @just --list
