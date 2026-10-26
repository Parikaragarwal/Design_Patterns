"""
Flyweight Pattern - Codebase Dependency Explorer
------------------------------------------------
Intent: Use sharing to support large numbers of fine-grained dependency relationship
edges efficiently by storing shared immutable state (intrinsic state) in Flyweights.
"""

from typing import Dict


class DependencyTypeFlyweight:
    """Flyweight containing intrinsic (shared) state for a dependency relationship."""
    
    def __init__(self, name: str, category: str, color_hex: str):
        self.name = name          # e.g., "IMPORT", "INHERITANCE", "CALLS"
        self.category = category  # e.g., "Static Dependency", "Dynamic Dependency"
        self.color_hex = color_hex # e.g., "#3498db"

    def render_edge(self, source: str, target: str) -> str:
        """Operation accepting extrinsic state (source and target names)."""
        return f"Edge({source} -> {target} | Type={self.name}, Category={self.category}, Color={self.color_hex})"


class DependencyTypeFlyweightFactory:
    """Flyweight Factory managing shared intrinsic instances."""
    
    _flyweights: Dict[str, DependencyTypeFlyweight] = {}

    @classmethod
    def get_dependency_type(cls, name: str, category: str = "Static Dependency", color_hex: str = "#cccccc") -> DependencyTypeFlyweight:
        key = name.upper()
        if key not in cls._flyweights:
            print(f"[FlyweightFactory] Creating NEW shared Flyweight instance for type '{key}'")
            cls._flyweights[key] = DependencyTypeFlyweight(key, category, color_hex)
        else:
            print(f"[FlyweightFactory] REUSING existing Flyweight instance for type '{key}'")
        return cls._flyweights[key]

    @classmethod
    def total_flyweights_created(cls) -> int:
        return len(cls._flyweights)
