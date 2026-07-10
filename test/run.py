from pathlib import Path
from spike import SpikeBackend
from zinc import ZincBackend
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "build" / "riscv-tests" / "isa"
SPIKE_BIN = ROOT / "build" / "spike" / "spike"
ZINC_BIN = ROOT / "build" / "zinc" / "sim" / "zinc-sim"

tests = sorted(
    p for p in TESTS_DIR.glob("rv64*-p-*")
        if p.suffix != ".dump"
)

golden_backend = SpikeBackend(SPIKE_BIN)
zinc_backend = ZincBackend(ZINC_BIN)

for test in tests:
    golden_commits = golden_backend.run(test)
    zinc_commits = zinc_backend.run(test)

    if len(golden_commits) != len(zinc_commits):
        raise RuntimeError(
            f"Commit count mismatch: in test {test}.dump"
            f"golden={len(golden_commits)}, zinc={len(zinc_commits)}"
        )

    for index, (golden_commit, zinc_commit) in enumerate(
        zip(golden_commits, zinc_commits)
    ):
        if golden_commit != zinc_commit:
            raise RuntimeError(
                f"Mismatch at commit {index} in test {test}.dump",
                f"Golden: {golden_commit}",
                f"Zinc: {zinc_commit}"
            )

    print(f"Finish all the test!")
