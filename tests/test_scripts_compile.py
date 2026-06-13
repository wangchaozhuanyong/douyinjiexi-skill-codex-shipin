import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_all_scripts_compile():
    for path in (ROOT / "scripts").glob("*.py"):
        py_compile.compile(str(path), doraise=True)
