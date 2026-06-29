from pathlib import Path
from common import Backend, Commit, RegWrite, MemAccess
import subprocess
import re

_LINE_RE = re.compile( r"^core\s+(\d+):\s+(\d+)\s+(0x[0-9a-f]+)\s+\((0x[0-9a-f]+)\)\s*(.*)$" )

def _parse_rest(rest: str):
    """把 (insn) 之后的尾巴切成 reg writes / mem reads / mem writes。"""
    tokens = rest.split()
    reg_writes: list[RegWrite] = []
    mem_reads: list[MemAccess] = []
    mem_writes: list[MemAccess] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == "mem":
            addr = int(tokens[i + 1], 16)
            # store: 地址后面还跟一个 value；load: 没有
            if i + 2 < len(tokens) and tokens[i + 2].startswith("0x"):
                mem_writes.append(
                    MemAccess(addr=addr, value=int(tokens[i + 2], 16), size=0)
                )
                i += 3
            else:
                mem_reads.append(MemAccess(addr=addr, value=0, size=0))
                i += 2
        else:
            # reg write: x5 / f10 / v2 ...  -> type=首字母, num=数字
            name = tok
            reg_writes.append(
                RegWrite(type=name[0], num=int(name[1:]), value=int(tokens[i + 1], 16))
            )
            i += 2
    return reg_writes, mem_reads, mem_writes

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

        ret: list[Commit] = []

        for line in r.stdout.splitlines():
            m = _LINE_RE.match(line)
            if not m:
                continue
            _hart, _priv, pc, insn, rest = m.groups()
            reg_writes, mem_reads, mem_writes = _parse_rest(rest)
            ret.append(
                Commit(
                    pc=int(pc, 16),
                    insn=int(insn, 16),
                    reg_writes=reg_writes,
                    mem_reads=mem_reads,
                    mem_writes=mem_writes
                )
            )

        return ret