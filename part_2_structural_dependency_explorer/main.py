"""
Part 2: Structural Design Patterns Demonstration
Topic: Codebase Dependency Explorer
------------------------------------------------
Demonstrates:
1. Adapter Pattern
2. Decorator Pattern
3. Composite Pattern
4. Facade Pattern
5. Bridge Pattern
6. Flyweight Pattern
7. Proxy Pattern
"""

from adapter import ExternalASTParser, LegacyLockfileParser, ASTDataAdapter, LockfileAdapter
from decorator import SimpleDependencyNode, MetricsDecorator, CircularDependencyWarningDecorator
from composite import PackageNode, SourceFileNode
from bridge import SimpleDependencyGraphView, ConsoleTreeRenderer, JSONExportRenderer
from flyweight import DependencyTypeFlyweightFactory
from proxy import LazyDependencyNodeProxy
from facade import CodebaseExplorerFacade


def print_banner(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_adapter():
    print_banner("1. ADAPTER PATTERN")
    print("Adapting external AST parser and legacy lockfile outputs...\n")

    ast_adapter = ASTDataAdapter("src/controllers/auth.py", ExternalASTParser())
    lock_adapter = LockfileAdapter("requests@2.31.0", LegacyLockfileParser())

    for adapter in [ast_adapter, lock_adapter]:
        print(f"-> Adapted Node ID:   {adapter.get_id()}")
        print(f"   Kind:              {adapter.get_kind()}")
        print(f"   Outgoing Deps:     {adapter.get_outgoing_dependencies()}\n")


def demo_decorator():
    print_banner("2. DECORATOR PATTERN")
    print("Dynamically adding metrics and circular dependency warnings...\n")

    base_node = SimpleDependencyNode("UserService", ["DatabasePool", "AuthService"])
    metrics_node = MetricsDecorator(base_node, loc=450, complexity=14)
    warning_node = CircularDependencyWarningDecorator(metrics_node, ["UserService", "AuthService", "UserService"])

    print("Details of fully decorated node:")
    import json
    print(json.dumps(warning_node.get_details(), indent=2))


def demo_composite():
    print_banner("3. COMPOSITE PATTERN")
    print("Building and rendering uniform directory/package hierarchy...\n")

    root = PackageNode("src")
    controllers = PackageNode("controllers")
    controllers.add(SourceFileNode("auth_controller.py", size_bytes=4200, lines=120))
    controllers.add(SourceFileNode("user_controller.py", size_bytes=3800, lines=95))

    services = PackageNode("services")
    services.add(SourceFileNode("payment_service.py", size_bytes=8900, lines=310))

    root.add(controllers)
    root.add(services)
    root.add(SourceFileNode("main.py", size_bytes=1500, lines=45))

    print(root.render())


def demo_facade():
    print_banner("4. FACADE PATTERN")
    print("Executing complex explorer workflows via simple Facade API...\n")

    facade = CodebaseExplorerFacade()
    
    print("Quick module analysis via Facade:")
    analysis = facade.quick_analyze_module("src/core/engine.py")
    print(f"   Name:    {analysis['name']}")
    print(f"   Metrics: {analysis.get('metrics')}\n")

    print("Package tree generation via Facade:")
    tree_out = facade.build_package_tree("utils_pkg", [
        ("logger.py", 1200, 40),
        ("formatter.py", 2300, 75)
    ])
    print(tree_out)


def demo_bridge():
    print_banner("5. BRIDGE PATTERN")
    print("Rendering dependency relations via decoupled Console and JSON renderers...\n")

    relations = [
        {"source": "AuthService", "target": "TokenManager", "type": "imports"},
        {"source": "TokenManager", "target": "CryptoUtils", "type": "calls"}
    ]

    console_view = SimpleDependencyGraphView(ConsoleTreeRenderer())
    json_view = SimpleDependencyGraphView(JSONExportRenderer())

    print("Console Renderer Output:")
    print(console_view.display("Auth Subsystem", relations))

    print("\nJSON Export Renderer Output (for Frontend UI):")
    print(json_view.display("Auth Subsystem", relations))


def demo_flyweight():
    print_banner("6. FLYWEIGHT PATTERN")
    print("Sharing intrinsic relation types across multiple dependency edges...\n")

    edges_data = [
        ("ModuleA", "ModuleB", "IMPORT"),
        ("ModuleC", "ModuleD", "IMPORT"),
        ("ClassX", "ClassY", "INHERITANCE"),
        ("ModuleE", "ModuleF", "IMPORT")
    ]

    for src, tgt, rel in edges_data:
        flyweight = DependencyTypeFlyweightFactory.get_dependency_type(rel, category="Static Import", color_hex="#16a085")
        print(f"  {flyweight.render_edge(src, tgt)}")

    print(f"\nTotal unique Flyweight objects created: {DependencyTypeFlyweightFactory.total_flyweights_created()}")


def demo_proxy():
    print_banner("7. PROXY PATTERN")
    print("Lazy-loading heavy AST dependencies on demand...\n")

    proxy_node = LazyDependencyNodeProxy("large_legacy_module.py")

    print("Proxy created. Heavy file NOT loaded yet.")
    print("\nRequesting dependencies first time:")
    deps1 = proxy_node.get_dependencies()
    print(f"   Result: {deps1}")

    print("\nRequesting dependencies second time (Cached):")
    deps2 = proxy_node.get_dependencies()
    print(f"   Result: {deps2}")


def main():
    print("============================================================")
    print("  CODEBASE DEPENDENCY EXPLORER - STRUCTURAL PATTERNS DEMO")
    print("============================================================")

    demo_adapter()
    demo_decorator()
    demo_composite()
    demo_facade()
    demo_bridge()
    demo_flyweight()
    demo_proxy()

    print_banner("ALL 7 STRUCTURAL PATTERNS EXECUTED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
