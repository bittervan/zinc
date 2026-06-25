from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "build" / "riscv-tests" / "isa"
SPIKE_BIN = ROOT / "build" / "spike" / "spike"

tests = sorted(
    p for p in TESTS_DIR.glob("rv64*-p-*")
        if p.suffix != ".dump"
)

for test in tests:
    r = subprocess.run([str(SPIKE_BIN), str(test)], capture_output=True, text=True)
    print(r.stderr)