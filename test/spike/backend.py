from pathlib import Path
from common import Backend, Commit, RegWrite, MemAccess
import subprocess
import re
from elftools.elf.elffile import ELFFile

_LINE_RE = re.compile( r"^core\s+(\d+):\s+(\d+)\s+(0x[0-9a-f]+)\s+\((0x[0-9a-f]+)\)\s*(.*)$" )
_REG_RE = re.compile(r"^([xfv])(\d+)$")
_CSR_RE = re.compile(r"^c(\d+)(?:_[A-Za-z0-9_]+)?$")

def _read_elf_entry(elf_path: Path) -> int:
    with elf_path.open("rb") as elf_file:
        elf = ELFFile(elf_file)
        return elf.header["e_entry"]

def _memory_access_size(insn: int) -> int:
    opcode = insn & 0x7f
    funct3 = (insn >> 12) & 0x7

    if opcode == 0b0000011:  # LOAD
        sizes = {
            0b000: 1,  # LB
            0b001: 2,  # LH
            0b010: 4,  # LW
            0b011: 8,  # LD
            0b100: 1,  # LBU
            0b101: 2,  # LHU
            0b110: 4,  # LWU
        }
    elif opcode == 0b0100011:  # STORE
        sizes = {
            0b000: 1,  # SB
            0b001: 2,  # SH
            0b010: 4,  # SW
            0b011: 8,  # SD
        }
    else:
        raise ValueError(
            f"memory trace for unsupported "
            f"instruction 0x{insn:08x}"
        )

    return sizes[funct3]

def _parse_rest(rest: str, insn):
    tokens = rest.split()
    reg_writes: list[RegWrite] = []
    mem_reads: list[MemAccess] = []
    mem_writes: list[MemAccess] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]

        if tok == "mem":
            addr = int(tokens[i + 1], 16)
            size = _memory_access_size(insn)

            if (
                i + 2 < len(tokens)
                and tokens[i + 2].startswith("0x")
            ):
                mem_writes.append(
                    MemAccess(
                        addr=addr,
                        value=int(tokens[i + 2], 16),
                        size=size,
                    )
                )
                i += 3
            else:
                mem_reads.append(
                    MemAccess(
                        addr=addr,
                        value=0,
                        size=size,
                    )
                )
                i += 2

        else:
            # reg write: x5 / f10 / v2 / c773_mtvec ...  -> type=首字母, num=数字
            m = _REG_RE.match(tok)
            if m:
                reg_type, reg_num = m.groups()
                reg_writes.append(
                    RegWrite(type=reg_type, num=int(reg_num), value=int(tokens[i + 1], 16))
                )
                i += 2
                continue

            m = _CSR_RE.match(tok)
            if m:
                reg_writes.append(
                    RegWrite(type="c", num=int(m.group(1)), value=int(tokens[i + 1], 16))
                )
                i += 2
                continue

    return reg_writes, mem_reads, mem_writes

class SpikeBackend(Backend):
    _bin_path: Path

    def __init__(self, bin_path: Path):
        self._bin_path = bin_path
        
    def run(self, elf_path: Path) -> list[Commit]:
        r = subprocess.run(
            [str(self._bin_path), "--priv=mu", "--triggers=0", f"--pc={_read_elf_entry(elf_path)}", "--log-commits", "--log=/dev/stdout", str(elf_path)],
            capture_output=True,
            text=True
        )

        ret: list[Commit] = []

        for line in r.stdout.splitlines():
            m = _LINE_RE.match(line)
            if not m:
                continue
            _hart, priv, pc, insn, rest = m.groups()

            reg_writes, mem_reads, mem_writes = _parse_rest(rest, int(insn, 16))
            ret.append(
                Commit(
                    pc=int(pc, 16),
                    insn=int(insn, 16),
                    priv=int(priv),
                    reg_writes=reg_writes,
                    mem_reads=mem_reads,
                    mem_writes=mem_writes
                )
            )

        return ret