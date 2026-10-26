# Part 2: Structural Design Patterns
## Domain: Codebase Dependency Explorer & AST Analyzer

This module implements all **7 Gang of Four (GoF) Structural Design Patterns** in clean, idiomatic Python. The project models a production-grade **Codebase Dependency Explorer**, designed to parse, aggregate, analyze, decorate, and visualize complex software architectures, ASTs, and package dependency graphs.

---

## 📑 Table of Contents
1. [Architecture & Directory Structure](#architecture--directory-structure)
2. [Design Patterns Overview Matrix](#design-patterns-overview-matrix)
3. [Deep-Dive Pattern Analysis & Implementation](#deep-dive-pattern-analysis--implementation)
   - [1. Adapter Pattern](#1-adapter-pattern)
   - [2. Decorator Pattern](#2-decorator-pattern)
   - [3. Composite Pattern](#3-composite-pattern)
   - [4. Facade Pattern](#4-facade-pattern)
   - [5. Bridge Pattern](#5-bridge-pattern)
   - [6. Flyweight Pattern](#6-flyweight-pattern)
   - [7. Proxy Pattern](#7-proxy-pattern)
4. [Running the Demonstration](#running-the-demonstration)
5. [🎙️ Viva Voce & Code Walkthrough Master Guide](#️-viva-voce--code-walkthrough-master-guide)
   - [General Structural Patterns Concept](#general-structural-patterns-concept)
   - [Pattern-by-Pattern Viva Speaking Scripts](#pattern-by-pattern-viva-speaking-scripts)
   - [Examiner Cross-Examination FAQ](#examiner-cross-examination-faq)

---

## Architecture & Directory Structure

```text
part_2_structural_dependency_explorer/
├── README.md           # Comprehensive documentation and viva guide
├── adapter.py          # Adapter: Harmonizes external AST & legacy lockfile outputs
├── decorator.py        # Decorator: Attaches metrics & circular dependency warnings
├── composite.py        # Composite: Hierarchical packages and leaf source files
├── facade.py           # Facade: Unified high-level API over all subsystems
├── bridge.py           # Bridge: Decouples graph views from console/JSON renderers
├── flyweight.py        # Flyweight: Pools immutable relationship types across edges
├── proxy.py            # Proxy: Lazy-loads expensive AST parsing on demand
└── main.py             # Integrated test harness & demonstration script
```

### File Responsibilities

| File | Primary Pattern | Key Classes / Interfaces | Core Responsibility |
| :--- | :--- | :--- | :--- |
| [`adapter.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py) | **Adapter** | `DependencyNode`, `ExternalASTParser`, `LegacyLockfileParser`, `ASTDataAdapter`, `LockfileAdapter` | Translates disparate third-party dictionary/tuple data into a standardized node interface. |
| [`decorator.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py) | **Decorator** | `BaseDependencyNode`, `SimpleDependencyNode`, `DependencyDecorator`, `MetricsDecorator`, `CircularDependencyWarningDecorator` | Dynamically wraps nodes with metrics and alerts without modifying base classes. |
| [`composite.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/composite.py) | **Composite** | `CodeArtifact`, `SourceFileNode` (Leaf), `PackageNode` (Composite) | Treats individual source files and nested package trees with uniform operations. |
| [`facade.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/facade.py) | **Facade** | `CodebaseExplorerFacade` | Shields clients from underlying subsystem complexity with simple helper methods. |
| [`bridge.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py) | **Bridge** | `GraphRenderer`, `ConsoleTreeRenderer`, `JSONExportRenderer`, `DependencyView`, `SimpleDependencyGraphView` | Allows visualization views and output formats to evolve independently. |
| [`flyweight.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/flyweight.py) | **Flyweight** | `DependencyTypeFlyweight`, `DependencyTypeFlyweightFactory` | Caches immutable relation attributes to prevent memory bloat on large graphs. |
| [`proxy.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/proxy.py) | **Proxy** | `DependencyGraphLoader`, `RealASTGraphLoader`, `LazyDependencyNodeProxy` | Postpones expensive disk I/O and AST parsing until dependencies are read. |
| [`main.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/main.py) | **Demo Driver** | `main()`, `demo_*()` functions | Comprehensive demo illustrating all 7 structural patterns in action. |

---

## Design Patterns Overview Matrix

```
+-----------------------------------------------------------------------------------------+
|                                STRUCTURAL DESIGN PATTERNS                               |
+---------------------+-------------------------------+-----------------------------------+
| Pattern             | GoF Intent                    | Role in Codebase Explorer Domain  |
+---------------------+-------------------------------+-----------------------------------+
| Adapter             | Convert interface of a class  | Unify incompatible third-party    |
|                     | to another interface expected | AST parser & legacy lockfiles     |
+---------------------+-------------------------------+-----------------------------------+
| Decorator           | Attach additional dynamic     | Augment nodes with metrics (LOC,  |
|                     | responsibilities to an object | complexity) & circular warnings   |
+---------------------+-------------------------------+-----------------------------------+
| Composite           | Compose objects into tree     | Uniformly represent packages      |
|                     | structures (part-whole)       | containing nested files & folders |
+---------------------+-------------------------------+-----------------------------------+
| Facade              | Unified high-level interface  | Simple API for multi-step module  |
|                     | to a subsystem of interfaces  | analysis & tree generation        |
+---------------------+-------------------------------+-----------------------------------+
| Bridge              | Decouple abstraction from     | Separate dependency view logic    |
|                     | implementation                | from Console / JSON renderers     |
+---------------------+-------------------------------+-----------------------------------+
| Flyweight           | Use sharing to support large  | Share immutable edge attributes   |
|                     | numbers of fine-grained objs  | (type, color) across 10,000+ edges|
+---------------------+-------------------------------+-----------------------------------+
| Proxy               | Surrogate/placeholder to      | Virtual proxy deferring expensive |
|                     | control access to an object   | disk parsing until access time    |
+---------------------+-------------------------------+-----------------------------------+
```

---

## Deep-Dive Pattern Analysis & Implementation

### 1. Adapter Pattern
- **Module**: [`adapter.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py)
- **GoF Intent**: "Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces."

#### Motivation & Problem Solved
Our explorer core expects all dependency nodes to adhere to [`DependencyNode`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py#L12-L26) (`get_id()`, `get_kind()`, `get_outgoing_dependencies()`). However:
- An external raw AST parser returns dictionaries: `{"module_name": ..., "ast_imports": ...}`.
- A legacy package lockfile parser returns raw tuples: `("requests-2.31.0", ["urllib3", ...])`.

Modifying those third-party libraries is impossible, and rewriting the explorer core to support custom types violates the Single Responsibility and Open/Closed principles. The Adapter wraps the incompatible interfaces into the target `DependencyNode`.

#### Implementation Structure
- **Target Interface**: [`DependencyNode`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py#L12-L26).
- **Adaptees**: [`ExternalASTParser`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py#L30-L39) and [`LegacyLockfileParser`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py#L43-L49).
- **Adapters**:
  - [`ASTDataAdapter`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py#L53-L67) wraps `ExternalASTParser.parse_file()`.
  - [`LockfileAdapter`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py#L69-L83) wraps `LegacyLockfileParser.parse_lock_entry()`.

---

### 2. Decorator Pattern
- **Module**: [`decorator.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py)
- **GoF Intent**: "Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality."

#### Motivation & Problem Solved
If we used inheritance to add features like code metrics (LOC, cyclomatic complexity) and circular dependency warnings to a node, we would suffer from a **combinatorial class explosion**:
- `SimpleNode`
- `NodeWithMetrics`
- `NodeWithWarnings`
- `NodeWithMetricsAndWarnings`
- `NodeWithSecurityAlerts` ... ($2^N$ subclasses for $N$ features!)

The Decorator pattern allows us to wrap any node dynamically at runtime in arbitrary combinations.

#### Implementation Structure
```
           +-------------------------+
           | <<abstract>>            |
           |   BaseDependencyNode    |
           +-------------------------+
           | + get_name(): str       |
           | + get_details(): dict   |
           +-------------------------+
                    ▲          ▲
                    |          |
  +-----------------+          +-----------------+
  |                                              |
+---------------------+               +-----------------------+
|SimpleDependencyNode |               |  DependencyDecorator  |
+---------------------+               +-----------------------+
                                      | - component: BaseNode |
                                      +-----------------------+
                                                  ▲
                                                  |
                                   +--------------+--------------+
                                   |                             |
                       +----------------------+      +-----------------------+
                       |   MetricsDecorator   |      | CircularDependencyWarn|
                       +----------------------+      +-----------------------+
```
- **Component Interface**: [`BaseDependencyNode`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py#L12-L22).
- **Concrete Component**: [`SimpleDependencyNode`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py#L24-L39).
- **Base Decorator**: [`DependencyDecorator`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py#L43-L54) implements `BaseDependencyNode` and forwards calls to its wrapped `_component`.
- **Concrete Decorators**:
  - [`MetricsDecorator`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py#L58-L74) appends `lines_of_code`, `cyclomatic_complexity`, and `coupling_rating`.
  - [`CircularDependencyWarningDecorator`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py#L76-L89) appends warning messages if circular loops are detected.

---

### 3. Composite Pattern
- **Module**: [`composite.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/composite.py)
- **GoF Intent**: "Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly."

#### Motivation & Problem Solved
Codebases are hierarchical: a directory can contain both source code files (leaves) and subdirectories (composites). Without Composite, client code traversing a codebase would constantly need type checks:
```python
# ANTI-PATTERN: Client branches on object type
if isinstance(item, File):
    total_size += item.file_size
elif isinstance(item, Directory):
    total_size += item.calculate_dir_size()
```
Composite defines a uniform interface (`render()`, `get_size_bytes()`) implemented by both leaves and composites.

#### Implementation Structure
- **Component**: [`CodeArtifact`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/composite.py#L13-L26).
- **Leaf**: [`SourceFileNode`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/composite.py#L28-L42) stores file lines and byte size.
- **Composite**: [`PackageNode`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/composite.py#L44-L67) holds `children: List[CodeArtifact]`. Its `get_size_bytes()` recursively sums its children's sizes, and `render(indent)` recursively formats the tree structure.

---

### 4. Facade Pattern
- **Module**: [`facade.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/facade.py)
- **GoF Intent**: "Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use."

#### Motivation & Problem Solved
Analyzing a module requires coordinating multiple disparate subsystems: parsing raw AST via `ExternalASTParser`, wrapping with `ASTDataAdapter`, creating a `SimpleDependencyNode`, and wrapping with `MetricsDecorator`.
For everyday client callers, this exposes unnecessary internal plumbing. The [`CodebaseExplorerFacade`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/facade.py#L17-L47) exposes simple 1-line methods:
- `quick_analyze_module(filepath)`
- `build_package_tree(root_name, files)`
- `render_graph_view(title, relations, json_format)`
- `lazy_load_dependencies(filepath)`

---

### 5. Bridge Pattern
- **Module**: [`bridge.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py)
- **GoF Intent**: "Decouple an abstraction from its implementation so that the two can vary independently."

#### Motivation & Problem Solved
We have two orthogonal dimensions that need to evolve independently:
1. **Views (Abstractions)**: Simple edge lists, detailed hierarchical graphs, dependency matrix views.
2. **Renderers (Implementations)**: Console terminal output, JSON output for frontend web UIs, SVG renderers, DOT graph formatters.

Inheritance causes a Cartesian explosion ($N \times M$ classes: `ConsoleSimpleView`, `JSONSimpleView`, `SVGSimpleView`, `ConsoleDetailedView`...).
Bridge decouples them: `DependencyView` holds a reference to a `GraphRenderer`, resulting in only $N + M$ classes.

#### Implementation Structure
- **Implementor Interface**: [`GraphRenderer`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py#L14-L28) (`render_header`, `render_edge`, `render_footer`).
- **Concrete Implementors**:
  - [`ConsoleTreeRenderer`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py#L32-L43) emits ASCII terminal graphs.
  - [`JSONExportRenderer`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py#L45-L56) emits JSON for web visualization.
- **Abstraction**: [`DependencyView`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py#L60-L69) receives a `GraphRenderer` via constructor dependency injection.
- **Refined Abstraction**: [`SimpleDependencyGraphView`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py#L73-L84).

---

### 6. Flyweight Pattern
- **Module**: [`flyweight.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/flyweight.py)
- **GoF Intent**: "Use sharing to support large numbers of fine-grained objects efficiently."

#### Motivation & Problem Solved
In a large enterprise codebase with 50,000 files and 200,000 dependency edges, each edge has relationship metadata:
- Relationship name: `"IMPORT"`, `"INHERITANCE"`, `"CALLS"`
- Category: `"Static Dependency"`, `"Dynamic Dependency"`
- Display Hex Color: `"#16a085"`, `"#e74c3c"`

Allocating 200,000 edge objects storing duplicate strings consumes hundreds of megabytes of RAM.
The Flyweight pattern splits state into:
1. **Intrinsic State (Shared & Immutable)**: The relation type, category, and color stored in [`DependencyTypeFlyweight`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/flyweight.py#L11-L22).
2. **Extrinsic State (Context-Dependent & Unique)**: The specific `source` and `target` nodes passed into `render_edge(source, target)`.

[`DependencyTypeFlyweightFactory`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/flyweight.py#L24-L42) pools and reuses these flyweights. Across hundreds of edges, only 2-3 flyweight instances are ever allocated in memory.

---

### 7. Proxy Pattern
- **Module**: [`proxy.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/proxy.py)
- **GoF Intent**: "Provide a surrogate or placeholder for another object to control access to it."

#### Motivation & Problem Solved
Parsing Python ASTs, resolving imports, and reading from disk is an expensive I/O and CPU operation. If the explorer loaded every module's AST at startup, the tool would experience significant launch latency.
[`LazyDependencyNodeProxy`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/proxy.py#L37-L51) acts as a **Virtual Proxy**:
- Instantiating the proxy is virtually instantaneous (it only stores the filepath).
- The heavy [`RealASTGraphLoader`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/proxy.py#L21-L35) is instantiated only when `get_dependencies()` is first invoked.
- Subsequent calls reuse the cached dependencies, bypassing disk and CPU overhead.

---

## Running the Demonstration

To execute the entire demonstration harness across all 7 patterns:

```bash
python3 part_2_structural_dependency_explorer/main.py
```

### Expected Output Summary
```text
============================================================
  CODEBASE DEPENDENCY EXPLORER - STRUCTURAL PATTERNS DEMO
============================================================

============================================================
  1. ADAPTER PATTERN
============================================================
-> Adapted Node ID:   src.controllers.auth
   Kind:              Python Module
   Outgoing Deps:     ['os', 'sys', 'json', 'typing.List']

-> Adapted Node ID:   requests-2.31.0
   Kind:              NPM/PyPI Package
   Outgoing Deps:     ['urllib3', 'certifi', 'charset-normalizer', 'idna']

============================================================
  2. DECORATOR PATTERN
============================================================
Details of fully decorated node:
{
  "name": "UserService",
  "dependencies": ["DatabasePool", "AuthService"],
  "metrics": {
    "lines_of_code": 450,
    "cyclomatic_complexity": 14,
    "coupling_rating": "High"
  },
  "warnings": [
    "CIRCULAR DEPENDENCY DETECTED: UserService -> AuthService -> UserService"
  ]
}

============================================================
  3. COMPOSITE PATTERN
============================================================
📁 src/ (18400 B total)
  📁 controllers/ (8000 B total)
    📄 auth_controller.py (120 lines, 4200 B)
    📄 user_controller.py (95 lines, 3800 B)
  📁 services/ (8900 B total)
    📄 payment_service.py (310 lines, 8900 B)
  📄 main.py (45 lines, 1500 B)

============================================================
  4. FACADE PATTERN
============================================================
Quick module analysis via Facade:
   Name:    src.core.engine
   Metrics: {'lines_of_code': 240, 'cyclomatic_complexity': 8, 'coupling_rating': 'Normal'}

============================================================
  5. BRIDGE PATTERN
============================================================
Console Renderer Output:
--- DEPENDENCY GRAPH: Auth Subsystem ---
  [AuthService] --(imports)--> [TokenManager]
  [TokenManager] --(calls)--> [CryptoUtils]
---------------------------------------

JSON Export Renderer Output (for Frontend UI):
{"title": "Auth Subsystem", "edges": [
  {"from": "AuthService", "to": "TokenManager", "relation": "imports"},
  {"from": "TokenManager", "to": "CryptoUtils", "relation": "calls"},
]}

============================================================
  6. FLYWEIGHT PATTERN
============================================================
[FlyweightFactory] Creating NEW shared Flyweight instance for type 'IMPORT'
  Edge(ModuleA -> ModuleB | Type=IMPORT, Category=Static Import, Color=#16a085)
[FlyweightFactory] REUSING existing Flyweight instance for type 'IMPORT'
  Edge(ModuleC -> ModuleD | Type=IMPORT, Category=Static Import, Color=#16a085)
[FlyweightFactory] Creating NEW shared Flyweight instance for type 'INHERITANCE'
  Edge(ClassX -> ClassY | Type=INHERITANCE, Category=Static Import, Color=#16a085)
[FlyweightFactory] REUSING existing Flyweight instance for type 'IMPORT'
  Edge(ModuleE -> ModuleF | Type=IMPORT, Category=Static Import, Color=#16a085)

Total unique Flyweight objects created: 2

============================================================
  7. PROXY PATTERN
============================================================
Proxy created. Heavy file NOT loaded yet.

Requesting dependencies first time:
[Proxy] Access requested for 'large_legacy_module.py'. Instantiating Real Object on demand...
  [HEAVY OPERATION] Parsing AST & reading disk file for 'large_legacy_module.py'...
   Result: ['large_legacy_module.py_dep1', 'large_legacy_module.py_dep2', 'core.utils']

Requesting dependencies second time (Cached):
[Proxy] Returning cached dependencies for 'large_legacy_module.py'.
   Result: ['large_legacy_module.py_dep1', 'large_legacy_module.py_dep2', 'core.utils']
```

---

## 🎙️ Viva Voce & Code Walkthrough Master Guide

Use this section when presenting this folder to an external examiner.

### General Structural Patterns Concept
> *"Good morning, examiner. In Part 2 of this project, I have implemented all 7 GoF Structural Design Patterns applied to a Codebase Dependency Explorer. Structural design patterns deal with object composition and class structure. They identify simple ways to realize relationships between entities, ensuring that when systems grow, parts can be reorganized or extended without breaking existing code."*

---

### Pattern-by-Pattern Viva Speaking Scripts

#### 1. Explaining Adapter ([`adapter.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/adapter.py))
- **What to say while showing the screen**:
  > *"Sir/Ma'am, in `adapter.py`, our explorer requires every node to implement `DependencyNode` with `get_id()`, `get_kind()`, and `get_outgoing_dependencies()`. However, third-party libraries return disparate formats: `ExternalASTParser` gives a Python dictionary, while `LegacyLockfileParser` gives raw tuples. I implemented two object adapters: `ASTDataAdapter` and `LockfileAdapter`. They wrap the adaptees and translate their outputs into our standard interface without modifying the third-party libraries."*

#### 2. Explaining Decorator ([`decorator.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/decorator.py))
- **What to say while showing the screen**:
  > *"Here in `decorator.py`, we want to dynamically attach code metrics (LOC, cyclomatic complexity) and circular dependency hazard warnings to a dependency node. If we used inheritance, we would suffer from a combinatorial class explosion of subclasses. Instead, `DependencyDecorator` implements `BaseDependencyNode` and wraps another `BaseDependencyNode`. As shown in `main.py`, I can wrap a `SimpleDependencyNode` inside a `MetricsDecorator`, and then wrap that inside a `CircularDependencyWarningDecorator`. The decorations nest cleanly at runtime."*

#### 3. Explaining Composite ([`composite.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/composite.py))
- **What to say while showing the screen**:
  > *"In `composite.py`, we represent the file tree hierarchy using the Composite pattern. Both `SourceFileNode` (Leaf) and `PackageNode` (Composite) inherit from `CodeArtifact`. A `PackageNode` contains a collection of child `CodeArtifact` objects. When calling `get_size_bytes()`, the composite recursively sums up the sizes of all its children. This allows the client to treat an individual file or an entire nested directory tree completely uniformly without writing type-checking `if-else` branches."*

#### 4. Explaining Facade ([`facade.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/facade.py))
- **What to say while showing the screen**:
  > *"In `facade.py`, I created `CodebaseExplorerFacade`. Our application has multiple sophisticated subsystems: Adapters, Composites, Decorators, Bridges, and Proxies. A typical client simply wants to analyze a file or generate a graph without manually wiring up AST parsers, adapters, and decorators. The facade provides clean, one-line entry points like `quick_analyze_module()` and `render_graph_view()`, adhering to the Principle of Least Knowledge."*

#### 5. Explaining Bridge ([`bridge.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/bridge.py))
- **What to say while showing the screen**:
  > *"In `bridge.py`, we have two independent dimensions of variation: the visualization view abstraction and the rendering implementation. Instead of creating a matrix of subclasses like `ConsoleSimpleGraphView` and `JSONSimpleGraphView`, Bridge decouples them. `DependencyView` holds a reference to the `GraphRenderer` implementor. By switching the renderer from `ConsoleTreeRenderer` to `JSONExportRenderer`, the exact same abstraction produces ASCII terminal output or JSON output for a web UI."*

#### 6. Explaining Flyweight ([`flyweight.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/flyweight.py))
- **What to say while showing the screen**:
  > *"In `flyweight.py`, we optimize memory for graphs with tens of thousands of edges. A dependency edge has intrinsic state—its type name, category, and color hex code—which is shared across thousands of edges. The extrinsic state consists of the specific source and target modules. `DependencyTypeFlyweightFactory` pools these flyweight objects. In our demo, four edge relationships are rendered, but only two flyweight instances are ever allocated in memory, saving massive RAM."*

#### 7. Explaining Proxy ([`proxy.py`](file:///home/parikar/DP-LabTest/part_2_structural_dependency_explorer/proxy.py))
- **What to say while showing the screen**:
  > *"Finally, in `proxy.py`, I implemented a Virtual Proxy: `LazyDependencyNodeProxy`. Parsing large ASTs from disk is an expensive I/O and CPU operation. The proxy implements `DependencyGraphLoader`. Upon instantiation, it does not touch the disk. Only when `get_dependencies()` is explicitly invoked does it instantiate the `RealASTGraphLoader`. On subsequent calls, it returns the cached result, avoiding redundant file parsing."*

---

### Examiner Cross-Examination FAQ

#### Q1: What is the key difference between Adapter and Facade?
**Answer**:
- **Adapter** makes two *incompatible existing interfaces* work together without changing their code. It wraps one interface to match another interface that the client already expects.
- **Facade** defines a *brand new, simplified interface* over an entire subsystem of classes to make them easier to use.

#### Q2: What is the difference between Proxy and Decorator? Both wrap an underlying object!
**Answer**:
- A **Decorator** focuses on *adding new responsibilities/behaviors* dynamically without altering the original class's interface. The client typically creates the component and chooses which decorators to wrap around it.
- A **Proxy** focuses on *controlling and managing access* to the underlying subject (e.g., lazy initialization, access control, caching). The client often interacts with the proxy directly without even knowing whether or when the real subject is instantiated.

#### Q3: In the Flyweight pattern, what is the difference between intrinsic and extrinsic state?
**Answer**:
- **Intrinsic State** is constant, immutable, and context-independent. It can be safely shared across many entities (e.g., relationship type `"IMPORT"`, category `"Static Import"`, and color `"#16a085"` stored inside `DependencyTypeFlyweight`).
- **Extrinsic State** is context-dependent and varies with every occurrence. It cannot be shared and is passed into the flyweight's methods by the caller (e.g., the specific `source` `"ModuleA"` and `target` `"ModuleB"` passed into `render_edge()`).

#### Q4: When should you use Composite over a standard list or dictionary of objects?
**Answer**:
Use **Composite** whenever the domain forms a natural part-whole tree hierarchy (like file systems, UI widget hierarchies, or organizational structures) and you want client code to invoke operations recursively on an entire tree or branch with the exact same method signature as an individual leaf element, without type checking.
