"""Compatibility entry point for the shared three-case resource audit."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('case-reader-links.py')),run_name='__main__')
