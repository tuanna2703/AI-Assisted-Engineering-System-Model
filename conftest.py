"""Root conftest — ensures the project root is on sys.path for all tests."""
import sys
from pathlib import Path

# Ensure the project root is importable.
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
