"""
Composite Pattern - Codebase Dependency Explorer
------------------------------------------------
Intent: Compose objects into tree structures to represent part-whole hierarchies
(packages, modules, source files). Allows clients to treat individual files and
entire directory packages uniformly.
"""

from abc import ABC, abstractmethod
from typing import List


class CodeArtifact(ABC):
    """Component: Abstract base for codebase tree entries."""
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def render(self, indent: int = 0) -> str:
        pass

    @abstractmethod
    def get_size_bytes(self) -> int:
        pass


class SourceFileNode(CodeArtifact):
    """Leaf: Represents an individual source code file."""
    
    def __init__(self, name: str, size_bytes: int, lines: int):
        super().__init__(name)
        self.size_bytes = size_bytes
        self.lines = lines

    def render(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}📄 {self.name} ({self.lines} lines, {self.size_bytes} B)"

    def get_size_bytes(self) -> int:
        return self.size_bytes


class PackageNode(CodeArtifact):
    """Composite: Represents a directory / package containing sub-artifacts."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[CodeArtifact] = []

    def add(self, artifact: CodeArtifact) -> 'PackageNode':
        self.children.append(artifact)
        return self

    def remove(self, artifact: CodeArtifact) -> None:
        self.children.remove(artifact)

    def render(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}📁 {self.name}/ ({self.get_size_bytes()} B total)"]
        for child in self.children:
            lines.append(child.render(indent + 1))
        return "\n".join(lines)

    def get_size_bytes(self) -> int:
        return sum(child.get_size_bytes() for child in self.children)
