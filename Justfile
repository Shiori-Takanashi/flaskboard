
# Justfile

# ==========================================
# Global Settings
# ==========================================


set shell := ["bash", "-euo", "pipefail", "-c"]

import 'just/dev.just'
import 'just/gcp.just'
import 'just/server.just'

TARGETS := "src tests"


# ==========================================
# Default Task
# ==========================================

default:
    @just --list
