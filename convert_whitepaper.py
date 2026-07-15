"""
convert_whitepaper.py — Convert project_part_2_whitepaper.ipynb to HTML
using nbconvert's Python API (avoids shell quoting issues on Windows).

Usage:
    python convert_whitepaper.py <notebook_path> <output_dir>

Tags used in the notebook:
  remove_cell    — entire cell hidden (instruction cells)
  remove_output  — cell output hidden (setup/status prints)
"""

import sys
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from traitlets.config import Config

notebook_path = sys.argv[1]
output_dir    = sys.argv[2]

# Build config
c = Config()
c.TagRemovePreprocessor.remove_cell_tags       = {'remove_cell'}
c.TagRemovePreprocessor.remove_all_outputs_tags = {'remove_output'}
c.TagRemovePreprocessor.enabled                = True
c.HTMLExporter.preprocessors                   = ['nbconvert.preprocessors.TagRemovePreprocessor']
c.HTMLExporter.exclude_input                   = True   # equivalent to --no-input

exporter = HTMLExporter(config=c)

with open(notebook_path, encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

body, _ = exporter.from_notebook_node(nb)

import os
out_path = os.path.join(output_dir, 'whitepaper.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(body)

print(f'[convert] Written {len(body):,} bytes to {out_path}')
