"""
Proxy Pattern - Codebase Dependency Explorer
--------------------------------------------
Intent: Provide a surrogate or placeholder (`LazyDependencyNodeProxy`) for another
object (`RealASTGraphLoader`) to control access to it, implementing lazy loading
for heavy file AST parsing.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class DependencyGraphLoader(ABC):
    """Subject Interface."""
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        pass


class RealASTGraphLoader(DependencyGraphLoader):
    """Real Subject: Performs heavy parsing of large codebase AST files."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._parse_ast()

    def _parse_ast(self) -> None:
        print(f"  [HEAVY OPERATION] Parsing AST & reading disk file for '{self.filepath}'...")
        # Simulating expensive parsing logic
        self._deps = [f"{self.filepath}_dep1", f"{self.filepath}_dep2", "core.utils"]

    def get_dependencies(self) -> List[str]:
        return self._deps


class LazyDependencyNodeProxy(DependencyGraphLoader):
    """Proxy: Postpones creation of RealASTGraphLoader until dependencies are requested."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._real_loader: RealASTGraphLoader = None

    def get_dependencies(self) -> List[str]:
        if self._real_loader is None:
            print(f"[Proxy] Access requested for '{self.filepath}'. Instantiating Real Object on demand...")
            self._real_loader = RealASTGraphLoader(self.filepath)
        else:
            print(f"[Proxy] Returning cached dependencies for '{self.filepath}'.")
        return self._real_loader.get_dependencies()
