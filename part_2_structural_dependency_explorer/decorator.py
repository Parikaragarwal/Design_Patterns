"""
Decorator Pattern - Codebase Dependency Explorer
------------------------------------------------
Intent: Attach additional responsibilities (metrics, circular dependency alerts)
to a dependency node dynamically without altering its underlying structure.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseDependencyNode(ABC):
    """Component Interface."""
    
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_details(self) -> Dict[str, Any]:
        pass


class SimpleDependencyNode(BaseDependencyNode):
    """Concrete Component representing a basic dependency node."""
    
    def __init__(self, name: str, dependencies: List[str]):
        self.name = name
        self.dependencies = list(dependencies)

    def get_name(self) -> str:
        return self.name

    def get_details(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "dependencies": self.dependencies
        }


# --- Base Decorator ---

class DependencyDecorator(BaseDependencyNode):
    """Decorator base class wrapping a BaseDependencyNode component."""
    
    def __init__(self, component: BaseDependencyNode):
        self._component = component

    def get_name(self) -> str:
        return self._component.get_name()

    def get_details(self) -> Dict[str, Any]:
        return self._component.get_details()


# --- Concrete Decorators ---

class MetricsDecorator(DependencyDecorator):
    """Concrete Decorator adding Code Quality & Complexity Metrics."""
    
    def __init__(self, component: BaseDependencyNode, loc: int, complexity: int):
        super().__init__(component)
        self.loc = loc
        self.complexity = complexity

    def get_details(self) -> Dict[str, Any]:
        details = super().get_details()
        details["metrics"] = {
            "lines_of_code": self.loc,
            "cyclomatic_complexity": self.complexity,
            "coupling_rating": "High" if self.complexity > 10 else "Normal"
        }
        return details


class CircularDependencyWarningDecorator(DependencyDecorator):
    """Concrete Decorator detecting circular dependency hazards."""
    
    def __init__(self, component: BaseDependencyNode, circular_path: List[str]):
        super().__init__(component)
        self.circular_path = circular_path

    def get_details(self) -> Dict[str, Any]:
        details = super().get_details()
        details["warnings"] = [
            f"CIRCULAR DEPENDENCY DETECTED: {' -> '.join(self.circular_path)}"
        ]
        return details
