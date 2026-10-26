"""
Bridge Pattern - Codebase Dependency Explorer
----------------------------------------------
Intent: Decouple an abstraction (`DependencyView`) from its implementation
(`GraphRenderer`) so that the two can vary independently.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


# --- Implementation Interface ---

class GraphRenderer(ABC):
    """Implementor interface defining primitive rendering operations."""
    
    @abstractmethod
    def render_header(self, graph_title: str) -> str:
        pass

    @abstractmethod
    def render_edge(self, source: str, target: str, rel_type: str) -> str:
        pass

    @abstractmethod
    def render_footer(self) -> str:
        pass


# --- Concrete Implementors ---

class ConsoleTreeRenderer(GraphRenderer):
    """Concrete Implementor for ASCII Terminal Output."""
    
    def render_header(self, graph_title: str) -> str:
        return f"--- DEPENDENCY GRAPH: {graph_title} ---"

    def render_edge(self, source: str, target: str, rel_type: str) -> str:
        return f"  [{source}] --({rel_type})--> [{target}]"

    def render_footer(self) -> str:
        return "---------------------------------------"


class JSONExportRenderer(GraphRenderer):
    """Concrete Implementor for JSON export (for frontend web visualization)."""
    
    def render_header(self, graph_title: str) -> str:
        return f'{{"title": "{graph_title}", "edges": ['

    def render_edge(self, source: str, target: str, rel_type: str) -> str:
        return f'  {{"from": "{source}", "to": "{target}", "relation": "{rel_type}"}},'

    def render_footer(self) -> str:
        return ']}'


# --- Abstraction ---

class DependencyView(ABC):
    """Abstraction: High-level view interface for dependency visualization."""
    
    def __init__(self, renderer: GraphRenderer):
        self.renderer = renderer

    @abstractmethod
    def display(self, graph_title: str, relations: List[Dict[str, str]]) -> str:
        pass


# --- Refined Abstractions ---

class SimpleDependencyGraphView(DependencyView):
    """Refined Abstraction for basic edge list viewing."""
    
    def display(self, graph_title: str, relations: List[Dict[str, str]]) -> str:
        output = [self.renderer.render_header(graph_title)]
        for rel in relations:
            output.append(self.renderer.render_edge(
                rel["source"], rel["target"], rel.get("type", "imports")
            ))
        output.append(self.renderer.render_footer())
        return "\n".join(output)
