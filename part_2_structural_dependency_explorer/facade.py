"""
Facade Pattern - Codebase Dependency Explorer
---------------------------------------------
Intent: Provide a unified high-level interface (`CodebaseExplorerFacade`) to a set
of complex subsystems (Adapter, Composite, Decorator, Bridge, Proxy, Flyweight).
"""

from typing import List, Dict, Any
from adapter import ExternalASTParser, ASTDataAdapter
from composite import PackageNode, SourceFileNode
from decorator import SimpleDependencyNode, MetricsDecorator, CircularDependencyWarningDecorator
from bridge import SimpleDependencyGraphView, ConsoleTreeRenderer, JSONExportRenderer
from flyweight import DependencyTypeFlyweightFactory
from proxy import LazyDependencyNodeProxy


class CodebaseExplorerFacade:
    """Facade: Simplifies interaction with all 6 underlying structural components."""
    
    def __init__(self):
        self.parser = ExternalASTParser()

    def quick_analyze_module(self, filepath: str) -> Dict[str, Any]:
        """Convenience method combining Adapter and Decorator subsystems."""
        adapter = ASTDataAdapter(filepath, self.parser)
        simple_node = SimpleDependencyNode(adapter.get_id(), adapter.get_outgoing_dependencies())
        decorated = MetricsDecorator(simple_node, loc=240, complexity=8)
        return decorated.get_details()

    def build_package_tree(self, root_name: str, files: List[tuple]) -> str:
        """Convenience method using Composite pattern."""
        root = PackageNode(root_name)
        for filename, size, lines in files:
            root.add(SourceFileNode(filename, size, lines))
        return root.render()

    def render_graph_view(self, title: str, relations: List[Dict[str, str]], json_format: bool = False) -> str:
        """Convenience method using Bridge pattern."""
        renderer = JSONExportRenderer() if json_format else ConsoleTreeRenderer()
        view = SimpleDependencyGraphView(renderer)
        return view.display(title, relations)

    def lazy_load_dependencies(self, filepath: str) -> List[str]:
        """Convenience method using Proxy pattern."""
        proxy = LazyDependencyNodeProxy(filepath)
        return proxy.get_dependencies()
