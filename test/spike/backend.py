from pathlib import Path
from common import Backend, Commit
import subprocess

class SpikeBackend(Backend):
    _bin_path: Path

    def __init__(self, bin_path: Path):
        self._bin_path = bin_path
        
    def run(self, elf_path: Path) -> list[Commit]:
        r = subprocess.run(
            [str(self._bin_path), "--log-commits", "--log=/dev/stdout", str(elf_path)],
            capture_output=True,
            text=True
        )

        print(r.stdout)

        return []