from dataclasses import dataclass

@dataclass
class RegWrite:
    type: str
    num: int
    value: int

    def __repr__(self):
        return (
            f"RegWrite(type={self.type!r}, "
            f"num={self.num}, "
            f"value=0x{self.value:016x})"
        )

@dataclass
class MemAccess:
    addr: int
    value: int
    size: int

    def __repr__(self):
        return (
            f"MemAccess(addr=0x{self.addr:016x}, "
            f"value=0x{self.value:016x}, "
            f"size={self.size})"
        )


@dataclass
class Commit:
    pc: int
    insn: int
    priv: int
    reg_writes: list[RegWrite]
    mem_reads: list[MemAccess]
    mem_writes: list[MemAccess]

    def __repr__(self):
        return (
            f"Commit(pc=0x{self.pc:016x}, "
            f"insn=0x{self.insn:08x}, "
            f"reg_writes={self.reg_writes}, "
            f"mem_reads={self.mem_reads}, "
            f"mem_writes={self.mem_writes})"
        )