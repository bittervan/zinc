from abc import ABC, abstractmethod
from .commit import Commit
from pathlib import Path

class Backend(ABC):
    _bin_path: Path
    
    @abstractmethod
    def __init__(self, bin_path: Path):
        raise NotImplementedError

    @abstractmethod
    def run(self, elf_path: Path) -> list[Commit]:
        raise NotImplementedError