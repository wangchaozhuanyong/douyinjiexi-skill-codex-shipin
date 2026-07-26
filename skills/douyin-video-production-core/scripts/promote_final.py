#!/usr/bin/env python3
"""Copy a pre-publish-gated video into final/final.mp4."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--package")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    package = Path(args.package).resolve() if args.package else project / "publish_package.json"
    gate = Path(__file__).with_name("pre_publish_gate.py")
    result = subprocess.run([sys.executable, str(gate), "--package", str(package)], check=False)
    if result.returncode:
        return result.returncode
    data = json.loads(package.read_text(encoding="utf-8"))
    source = Path(data["video"])
    target = project / "final" / "final.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(json.dumps({"status": "promoted", "final": str(target)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
