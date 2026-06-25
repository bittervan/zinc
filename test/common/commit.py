from dataclasses import dataclass

@dataclass
class RegWrite:
    type: str
    num: int
    value: int

@dataclass
class MemAccess:
    addr: int
    value: int
    size: int

@dataclass
class Commit:
    pc: int
    insn: int
    reg_writes: list[RegWrite]
    mem_reads: list[MemAccess]
    mem_writes: list[MemAccess]