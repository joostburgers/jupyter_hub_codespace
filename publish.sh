#!/bin/bash
# Publishes the Project 5 website to GitHub Pages.
# Run from the Codespaces terminal (from anywhere inside the repo):
#   bash publish.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/project_5_mapping_emotions/publish.sh"
