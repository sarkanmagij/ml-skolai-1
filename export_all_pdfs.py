#!/usr/bin/env python3
"""Export each numbered-folder notebook to WebPDF.

By default runs ``--execute`` so PDFs include outputs (run from each notebook's folder
so relative paths like ``bank.csv`` work). Pass ``--no-execute`` to skip execution.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# One notebook per module folder (sorted by folder name)
NOTEBOOKS: list[tuple[str, Path]] = [
    ("1", ROOT / "1/02_EDA_Penguins_assignment_unsolved.ipynb"),
    ("2", ROOT / "2/05_LinearRegression_AutoMPG_unsolved.ipynb"),
    ("3", ROOT / "3/06_LogisticRegression_Iris_unsolved.ipynb"),
    ("4", ROOT / "4/07_decision_trees_exercise.ipynb"),
    ("5", ROOT / "5/08_Exercise_02_RandomForest_RockOrMine_UNSOLVED (1).ipynb"),
    ("6", ROOT / "6/11_XGBoost_unsolved.ipynb"),
    ("7", ROOT / "7/GBM_Comparison_UNSOLVED.ipynb"),
    ("8", ROOT / "8/09_k-means_unsolved.ipynb"),
    ("9", ROOT / "9/Exercise_PCA_Basics_UNSOLVED (1).ipynb"),
    ("10", ROOT / "10/13_Prophet_unsolved (1).ipynb"),
]


def main() -> int:
    execute = "--no-execute" not in sys.argv
    fail = 0
    for _folder, nb_path in NOTEBOOKS:
        if not nb_path.is_file():
            print(f"Skip (missing): {nb_path}")
            fail += 1
            continue
        cwd = nb_path.parent
        cmd = [sys.executable, "-m", "jupyter", "nbconvert"]
        if execute:
            cmd += ["--execute", "--ExecutePreprocessor.timeout=900"]
        cmd += ["--to", "webpdf", nb_path.name]
        print(f"\n>>> {' '.join(cmd)} (cwd={cwd})")
        env = os.environ.copy()
        r = subprocess.run(cmd, cwd=cwd, env=env)
        if r.returncode != 0:
            print(f"FAILED: {nb_path.name}", file=sys.stderr)
            fail += 1
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
