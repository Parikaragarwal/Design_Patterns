"""
Adapter Pattern - Codebase Dependency Explorer
----------------------------------------------
Intent: Convert the interface of external legacy AST and lockfile parsers into
a unified `DependencyNode` interface that the codebase explorer expects.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple


class DependencyNode(ABC):
    """Target Interface expected by the explorer."""
    
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_kind(self) -> str:
        pass

    @abstractmethod
    def get_outgoing_dependencies(self) -> List[str]:
        pass


# --- Adaptee 1: External Raw AST Parser Output ---

class ExternalASTParser:
    """Adaptee: An external library that returns raw dictionary data."""
    
    def parse_file(self, filepath: str) -> Dict[str, Any]:
        return {
            "module_name": filepath.replace("/", ".").replace(".py", ""),
            "ast_imports": ["os", "sys", "json", "typing.List"],
            "defined_classes": ["ASTExplorerNode"]
        }


# --- Adaptee 2: Legacy Lockfile Parser Output ---

class LegacyLockfileParser:
    """Adaptee: A legacy parser returning raw tuple pairs."""
    
    def parse_lock_entry(self, package_entry: str) -> Tuple[str, List[str]]:
        # Returns (package_name, [dependency_names])
        return ("requests-2.31.0", ["urllib3", "certifi", "charset-normalizer", "idna"])


# --- Adapters ---

class ASTDataAdapter(DependencyNode):
    """Adapter for ExternalASTParser."""
    
    def __init__(self, filepath: str, external_parser: ExternalASTParser):
        self.raw_data = external_parser.parse_file(filepath)

    def get_id(self) -> str:
        return self.raw_data["module_name"]

    def get_kind(self) -> str:
        return "Python Module"

    def get_outgoing_dependencies(self) -> List[str]:
        return self.raw_data["ast_imports"]


class LockfileAdapter(DependencyNode):
    """Adapter for LegacyLockfileParser."""
    
    def __init__(self, package_entry: str, legacy_parser: LegacyLockfileParser):
        self.pkg_name, self.deps = legacy_parser.parse_lock_entry(package_entry)

    def get_id(self) -> str:
        return self.pkg_name

    def get_kind(self) -> str:
        return "NPM/PyPI Package"

    def get_outgoing_dependencies(self) -> List[str]:
        return self.deps
