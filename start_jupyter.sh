#!/bin/bash
# Startup script for running Jupyter in Codespace
# This script configures Jupyter to be accessible via the Codespace port-forwarding

echo "🚀 Starting Jupyter Notebook Server..."
echo ""
echo "Your Jupyter notebook will be available in the Codespace ports panel."
echo "If you don't see it, check the 'Ports' tab at the bottom of the VS Code window."
echo ""

jupyter notebook \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --NotebookApp.token='' \
    --NotebookApp.password=''
