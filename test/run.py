from pathlib import Path
from spike import SpikeBackend
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "build" / "riscv-tests" / "isa"
SPIKE_BIN = ROOT / "build" / "spike" / "spike"

tests = sorted(
    p for p in TESTS_DIR.glob("rv64*-p-*")
        if p.suffix != ".dump"
)

golden_backend = SpikeBackend(SPIKE_BIN)

for test in tests:
    golden_commits = golden_backend.run(test)
    print(golden_commits)