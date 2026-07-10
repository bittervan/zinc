from common import Backend, Commit, RegWrite, MemAccess
from pathlib import Path
import subprocess
import json

class ZincBackend(Backend):
    _bin_path: Path

    def __init__(self, bin_path: Path):
        self._bin_path = bin_path
    
    def run(self, elf_path: Path) -> list[Commit]:
        r = subprocess.run(
            [str(self._bin_path), str(elf_path)],
            capture_output=True,
            text=True
        )

        if r.returncode != 0:
            raise RuntimeError(
                f"failed to run {elf_path}: {r.stderr.rstrip()}"
            )

        ret: list[Commit] = []
        
        for line in r.stdout.splitlines():
            data = json.loads(line)
            commit = Commit(
                pc=int(data["pc"], 0),
                insn=int(data["insn"], 0),
                reg_writes=[
                    RegWrite(
                        type=write["type"],
                        num=write["num"],
                        value=write["value"]
                    ) for write in data["reg_writes"]
                ],
                mem_reads=[
                    MemAccess(
                        addr=read["addr"],
                        value=read["value"],
                        size=read["size"],
                    ) for read in data["mem_reads"]
                ],
                mem_writes=[
                    MemAccess(
                        addr=read["addr"],
                        value=read["value"],
                        size=read["size"],
                    ) for read in data["mem_writes"]
                ]
            )

            ret.append(commit)

        return ret