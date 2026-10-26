# Part 1: Creational Design Patterns
## Domain: CI/CD Pipeline Visualizer & Orchestrator

This module implements all **5 Gang of Four (GoF) Creational Design Patterns** in clean, idiomatic Python. The project models a modern **CI/CD Pipeline Visualizer**, solving real-world software design challenges such as dynamic stage instantiation, multi-cloud provider compatibility, step-by-step pipeline construction, global state registry, and reusable pipeline templating.

---

## 📑 Table of Contents
1. [Architecture & Directory Structure](#architecture--directory-structure)
2. [Design Patterns Overview Matrix](#design-patterns-overview-matrix)
3. [Deep-Dive Pattern Analysis & Implementation](#deep-dive-pattern-analysis--implementation)
   - [1. Factory Method Pattern](#1-factory-method-pattern)
   - [2. Abstract Factory Pattern](#2-abstract-factory-pattern)
   - [3. Builder Pattern](#3-builder-pattern)
   - [4. Singleton Pattern](#4-singleton-pattern)
   - [5. Prototype Pattern](#5-prototype-pattern)
4. [Running the Demonstration](#running-the-demonstration)
5. [🎙️ Viva Voce & Code Walkthrough Master Guide](#️-viva-voce--code-walkthrough-master-guide)
   - [General Creational Patterns Concept](#general-creational-patterns-concept)
   - [Pattern-by-Pattern Viva Speaking Scripts](#pattern-by-pattern-viva-speaking-scripts)
   - [Examiner Cross-Examination FAQ](#examiner-cross-examination-faq)

---

## Architecture & Directory Structure

```text
part_1_creational_cicd_pipeline/
├── README.md               # Comprehensive documentation and viva guide
├── factory_method.py       # Factory Method: Stage creation abstraction
├── abstract_factory.py     # Abstract Factory: Multi-provider toolchains (GitHub vs GitLab)
├── builder.py              # Builder: Step-by-step pipeline assembly & presets
├── singleton.py            # Singleton: Thread-safe global configuration registry
├── prototype.py            # Prototype: Deep-cloned microservice & container templates
└── main.py                 # Integrated test harness & demonstration script
```

### File Responsibilities

| File | Primary Pattern | Key Classes / Interfaces | Core Responsibility |
| :--- | :--- | :--- | :--- |
| [`factory_method.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py) | **Factory Method** | `PipelineStage`, `BuildStage`, `TestStage`, `DeployStage`, `PipelineStageFactory` | Decouples stage execution logic from concrete stage instantiation. |
| [`abstract_factory.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py) | **Abstract Factory** | `JobRunner`, `ConfigFormatter`, `CIPipelineProviderFactory`, `GitHubActionsFactory`, `GitLabCIFactory` | Produces families of compatible CI runner and formatter objects. |
| [`builder.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/builder.py) | **Builder** | `Pipeline`, `PipelineBuilder`, `PipelineDirector` | Constructs complex, configurable multi-stage pipelines step-by-step. |
| [`singleton.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/singleton.py) | **Singleton** | `PipelineConfigRegistry` | Guarantees a single, thread-safe global registry for visualizer settings. |
| [`prototype.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/prototype.py) | **Prototype** | `PipelineTemplate`, `PythonServiceTemplate`, `DockerServiceTemplate` | Creates new pipeline configs by deep-copying pre-configured templates. |
| [`main.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/main.py) | **Demo Driver** | `main()`, `demo_*()` functions | Orchestrates and prints verification output for all 5 patterns. |

---

## Design Patterns Overview Matrix

```
+-----------------------------------------------------------------------------------------+
|                                CREATIONAL DESIGN PATTERNS                               |
+---------------------+-------------------------------+-----------------------------------+
| Pattern             | GoF Intent                    | Role in CI/CD Pipeline Domain     |
+---------------------+-------------------------------+-----------------------------------+
| Factory Method      | Defer instantiation to        | Create polymorphic stages         |
|                     | subclasses                    | (Build, Test, Deploy)             |
+---------------------+-------------------------------+-----------------------------------+
| Abstract Factory    | Create families of related or | Produce matching runner + YAML    |
|                     | dependent objects             | formatter per CI provider         |
+---------------------+-------------------------------+-----------------------------------+
| Builder             | Separate complex construction | Construct multi-stage pipelines   |
|                     | from representation           | with timeouts, env vars, hooks    |
+---------------------+-------------------------------+-----------------------------------+
| Singleton           | Ensure single instance with   | Centralize global settings,       |
|                     | global access point           | concurrency limits & UI themes    |
+---------------------+-------------------------------+-----------------------------------+
| Prototype           | Create new objects by cloning | Rapidly spawn customized service  |
|                     | an existing instance          | pipelines from base templates     |
+---------------------+-------------------------------+-----------------------------------+
```

---

## Deep-Dive Pattern Analysis & Implementation

### 1. Factory Method Pattern
- **Module**: [`factory_method.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py)
- **GoF Intent**: "Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses."

#### Motivation & Problem Solved
Without the Factory Method, client code would directly instantiate concrete classes using `if-elif-else` branches:
```python
# ANTI-PATTERN: Direct coupling & violates Open/Closed Principle
if stage_type == "build":
    stage = BuildStage(name)
elif stage_type == "test":
    stage = TestStage(name)
```
Every time a new stage (e.g., `SecurityScanStage` or `LintStage`) is introduced, the client code must be modified, risking regressions. Factory Method enforces the **Open/Closed Principle (OCP)**: existing code remains closed for modification but open for extension through new factory subclasses.

#### Implementation Structure
```
       +-----------------------+              +------------------------+
       | <<abstract>>          |              | <<abstract>>           |
       |     PipelineStage     |              |  PipelineStageFactory  |
       +-----------------------+              +------------------------+
       | + execute(): dict     |              | + create_stage(): Stage|
       +-----------------------+              | + run_stage(): dict    |
                  ▲                           +------------------------+
                  |                                       ▲
     +------------+------------+                          |
     |            |            |             +------------+------------+
+---------+  +---------+  +----------+       |            |            |
|BuildStg |  | TestStg |  |DeployStg |  +----------+ +---------+ +-----------+
+---------+  +---------+  +----------+  |BuildFact | |TestFact | |DeployFact |
                                        +----------+ +---------+ +-----------+
```

- **Abstract Product**: [`PipelineStage`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L12-L22) defines the common interface (`execute()`) and lifecycle state.
- **Concrete Products**: [`BuildStage`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L24-L35), [`TestStage`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L37-L48), and [`DeployStage`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L50-L61).
- **Abstract Creator**: [`PipelineStageFactory`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L65-L76) declares the factory method `create_stage(name)` and provides business logic `run_stage(name)`.
- **Concrete Creators**: [`BuildStageFactory`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L78-L83), [`TestStageFactory`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L85-L90), [`DeployStageFactory`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py#L92-L97).

---

### 2. Abstract Factory Pattern
- **Module**: [`abstract_factory.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py)
- **GoF Intent**: "Provide an interface for creating families of related or dependent objects without specifying their concrete classes."

#### Motivation & Problem Solved
A visualizer must support multiple CI platforms (e.g., GitHub Actions vs. GitLab CI). Each platform requires a compatible pair of objects:
1. A **JobRunner** (to execute jobs on specific runner infrastructure).
2. A **ConfigFormatter** (to emit syntax-valid YAML configuration).

If client code independently instantiated `GitHubActionsRunner` with `GitLabYAMLFormatter`, the pipeline would crash at runtime due to vendor format mismatches. Abstract Factory guarantees that product families always match.

#### Implementation Structure
```
            +------------------------------------+
            | <<abstract>>                       |
            |     CIPipelineProviderFactory      |
            +------------------------------------+
            | + create_runner(): JobRunner       |
            | + create_formatter(): ConfigFormat |
            +------------------------------------+
                              ▲
                              |
               +--------------+--------------+
               |                             |
     +--------------------+       +--------------------+
     |GitHubActionsFactory|       |  GitLabCIFactory   |
     +--------------------+       +--------------------+
     | creates:           |       | creates:           |
     | - GitHubActionsRun |       | - GitLabCIRunner   |
     | - GitHubYAMLFormat |       | - GitLabYAMLFormat |
     +--------------------+       +--------------------+
```

- **Abstract Products**: [`JobRunner`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L14-L20) and [`ConfigFormatter`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L22-L28).
- **Concrete Products (GitHub)**: [`GitHubActionsRunner`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L32-L35) and [`GitHubYAMLFormatter`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L37-L41).
- **Concrete Products (GitLab)**: [`GitLabCIRunner`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L45-L48) and [`GitLabYAMLFormatter`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L50-L54).
- **Abstract Factory**: [`CIPipelineProviderFactory`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L58-L68).
- **Concrete Factories**: [`GitHubActionsFactory`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L72-L80) and [`GitLabCIFactory`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py#L82-L90).

---

### 3. Builder Pattern
- **Module**: [`builder.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/builder.py)
- **GoF Intent**: "Separate the construction of a complex object from its representation so that the same construction process can create different representations."

#### Motivation & Problem Solved
A `Pipeline` object has numerous optional attributes: stages, environment variables, timeouts, and alert webhooks. Instantiating it via a constructor creates the **Telescoping Constructor Anti-Pattern**:
```python
# ANTI-PATTERN: Telescoping constructor with unreadable optional arguments
p = Pipeline("Auth", ["build", "test"], {"ENV": "prod"}, 45, "http://...", True, False, 3, None)
```
Builder allows step-by-step construction using method chaining (Fluent Interface), while the **Director** encapsulates reusable assembly recipes.

#### Implementation Structure
- **Product**: [`Pipeline`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/builder.py#L11-L33) represents the assembled configuration.
- **Builder**: [`PipelineBuilder`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/builder.py#L35-L69) maintains internal state, provides methods returning `self` for chaining (`set_name`, `add_stage`, `set_environment_variable`, `set_timeout`, `set_notification_webhook`), and a final `build()` method.
- **Director**: [`PipelineDirector`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/builder.py#L71-L98) exposes predefined creation routines:
  - `build_standard_microservice_pipeline(name)` (Checkout -> Compile -> Docker -> Security Scan -> Deploy)
  - `build_fast_ci_pipeline(name)` (Checkout -> Linter & Fast Unit Test)

---

### 4. Singleton Pattern
- **Module**: [`singleton.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/singleton.py)
- **GoF Intent**: "Ensure a class only has one instance, and provide a global point of access to it."

#### Motivation & Problem Solved
Global settings such as visualizer theme (`"Dark-Neon"`), concurrency limits (`max_parallel_jobs`), and retry policies must be consistent across all worker threads and stages. Multiple uncoordinated config instances would lead to synchronization bugs and race conditions.

#### Implementation Structure
[`PipelineConfigRegistry`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/singleton.py#L12-L40) uses Python's `__new__` method combined with a thread lock:
1. `_instance = None` holds the single allocated object.
2. `_lock = threading.Lock()` guarantees thread safety during instantiation.
3. If `_instance` is None, `super().__new__(cls)` allocates the instance and populates default settings.
4. Subsequent calls return the existing `_instance`.

---

### 5. Prototype Pattern
- **Module**: [`prototype.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/prototype.py)
- **GoF Intent**: "Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype."

#### Motivation & Problem Solved
Building a 10-stage containerized pipeline configuration from scratch with full environment variables is computationally redundant when hundreds of microservices share 90% of the same steps.
Prototype enables cloning a pre-configured template (`PythonServiceTemplate` or `DockerServiceTemplate`) and altering only the specific deltas (e.g., adding a custom test stage).

#### Implementation Structure
- **Abstract Prototype**: [`PipelineTemplate`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/prototype.py#L13-L31) declares `clone()` and common serialization helper `to_dict()`.
- **Concrete Prototypes**:
  - [`PythonServiceTemplate`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/prototype.py#L33-L46)
  - [`DockerServiceTemplate`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/prototype.py#L48-L61)
- **Deep Copy**: Both classes implement `copy.deepcopy(self)`. Deep copying is critical because pipelines contain mutable nested lists (`stages`) and dictionaries (`env_vars`). A shallow copy would cause modifications in a clone to mutate the original template!

---

## Running the Demonstration

To execute the entire demonstration harness across all 5 patterns:

```bash
python3 part_1_creational_cicd_pipeline/main.py
```

### Expected Output Summary
```text
============================================================
   CI/CD PIPELINE VISUALIZER - CREATIONAL PATTERNS DEMO
============================================================

============================================================
  1. FACTORY METHOD PATTERN
============================================================
Creating and executing stages using stage factories...

-> Created Stage [Build]: Compilation Step
   Status:  Completed
   Details: Compiled source code into distribution binary artifact.
...

============================================================
  2. ABSTRACT FACTORY PATTERN
============================================================
[GitHub Actions Provider Family]
   Runner:    [GitHub Actions Runner] Executing workflow job 'Integration Test Job'...
   Config preview:
     | name: Payment Microservice CI
     | on: [push, pull_request]

[GitLab CI Provider Family]
   Runner:    [GitLab CI Runner] Executing pipeline job 'Integration Test Job'...
...

============================================================
  3. BUILDER PATTERN
============================================================
Pipeline A: Pipeline('Auth Service Pipeline', Stages=[Checkout Code -> Compile & Unit Test -> Build Docker Image -> Security Vulnerability Scan -> Deploy to Staging], Timeout=45m)
...

============================================================
  4. SINGLETON PATTERN
============================================================
Are reg1 and reg2 the exact same instance? YES
Modifying configuration via reg1...
Updated Config retrieved from reg2: {'max_parallel_jobs': 8, 'logging_level': 'DEBUG', ...}

============================================================
  5. PROTOTYPE PATTERN
============================================================
Original Prototype: {'template_name': 'Python Microservice Standard', 'stages': [...5 stages...]}
Cloned & Modified:  {'template_name': 'Customized User-Service Pipeline', 'stages': [...6 stages including SonarQube...]}
```

---

## 🎙️ Viva Voce & Code Walkthrough Master Guide

Use this section when presenting this folder to an external examiner.

### General Creational Patterns Concept
> *"Good morning, examiner. In Part 1 of this laboratory work, I have modeled a CI/CD Pipeline Visualizer using all 5 GoF Creational Design Patterns. Creational patterns abstract the object instantiation process. They make the system independent of how its objects are created, composed, and represented, promoting the Open/Closed Principle and loose coupling."*

---

### Pattern-by-Pattern Viva Speaking Scripts

#### 1. Explaining Factory Method ([`factory_method.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/factory_method.py))
- **What to say while showing the screen**:
  > *"Sir/Ma'am, here in `factory_method.py`, I have defined an abstract product `PipelineStage` with concrete subclasses `BuildStage`, `TestStage`, and `DeployStage`. Instead of directly calling `BuildStage()` in my client code with an `if-else` condition, I created an abstract creator `PipelineStageFactory` with a factory method `create_stage()`. Each concrete factory—like `BuildStageFactory`—overrides this method to instantiate its corresponding stage. This enforces the Open/Closed Principle: if we need to add a new `LintStage`, we simply add `LintStage` and `LintStageFactory` without touching existing factory code."*

#### 2. Explaining Abstract Factory ([`abstract_factory.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/abstract_factory.py))
- **What to say while showing the screen**:
  > *"Now moving to `abstract_factory.py`. While Factory Method creates a single product, Abstract Factory creates families of related products. Here, a CI platform requires two distinct components: a `JobRunner` and a `ConfigFormatter`. The `CIPipelineProviderFactory` defines methods for both. `GitHubActionsFactory` produces a `GitHubActionsRunner` and a `GitHubYAMLFormatter`. `GitLabCIFactory` produces the GitLab equivalents. The benefit is architectural safety: a client cannot accidentally mix a GitHub runner with a GitLab YAML config. The family consistency is enforced at compile/instantiation time."*

#### 3. Explaining Builder ([`builder.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/builder.py))
- **What to say while showing the screen**:
  > *"In `builder.py`, I implemented the Builder pattern. A `Pipeline` is a complex object consisting of multiple stages, environment variables, timeouts, and webhooks. Passing all of these through a single constructor leads to the Telescoping Constructor anti-pattern. `PipelineBuilder` provides a fluent interface where each method returns `self`, allowing chaining. Furthermore, I created a `PipelineDirector` class that encapsulates standard recipes, such as `build_standard_microservice_pipeline()` and `build_fast_ci_pipeline()`, hiding construction complexity from the caller."*

#### 4. Explaining Singleton ([`singleton.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/singleton.py))
- **What to say while showing the screen**:
  > *"In `singleton.py`, I implemented `PipelineConfigRegistry` to store global visualizer settings like `max_parallel_jobs` and UI themes. To ensure thread safety in a multi-threaded CI environment, I protected the `__new__` method with a `threading.Lock()`. If you observe our demonstration in `main.py`, `reg1` and `reg2` point to the exact same memory address (`reg1 is reg2` is True). When I mutate a setting in `reg1`, it is immediately reflected when querying `reg2`."*

#### 5. Explaining Prototype ([`prototype.py`](file:///home/parikar/DP-LabTest/part_1_creational_cicd_pipeline/prototype.py))
- **What to say while showing the screen**:
  > *"Finally, in `prototype.py`, I demonstrated the Prototype pattern using `PythonServiceTemplate` and `DockerServiceTemplate`. When spinning up dozens of similar microservice pipelines, re-specifying all stages from scratch is redundant. Here, we clone an existing prototype via `copy.deepcopy(self)`. Deep copy is crucial because lists and dictionaries in Python are mutable references; a shallow copy would cause changes in a cloned pipeline to unintentionally mutate the original prototype template."*

---

### Examiner Cross-Examination FAQ

#### Q1: What is the primary difference between Factory Method and Abstract Factory?
**Answer**:
- **Factory Method** uses inheritance and produces **one product**. A single factory method in a creator is overridden by subclasses to create a single object (e.g., `BuildStageFactory` creates `BuildStage`).
- **Abstract Factory** uses composition and produces **families of related products**. It defines multiple factory methods (e.g., `create_runner()` and `create_formatter()`) to guarantee that created products are mutually compatible.

#### Q2: Why did you use `__new__` instead of `__init__` for the Singleton?
**Answer**:
In Python, `__new__` is the actual constructor responsible for creating and returning a new object instance, whereas `__init__` merely initializes an already created instance. If we implement Singleton logic inside `__init__`, Python will still invoke `__init__` on every call to `PipelineConfigRegistry()`, re-initializing the dictionary and wiping out existing state. Overriding `__new__` allows us to return the cached `_instance` directly.

#### Q3: Why is `copy.deepcopy()` necessary in the Prototype pattern?
**Answer**:
A standard assignment or shallow copy (`copy.copy()`) only copies the top-level object reference; internal references to mutable objects (like the `stages` list or `env_vars` dictionary) remain shared. If a clone appends a new stage, the original prototype's stages would also be modified. `copy.deepcopy()` recursively copies all nested objects, ensuring total memory isolation.

#### Q4: When would you choose Builder over Abstract Factory?
**Answer**:
Choose **Builder** when the object is complex and must be constructed step-by-step through a sequence of operations with various permutations of configuration. Choose **Abstract Factory** when the creation is single-step, but you need to ensure that multiple distinct products belong to the same compatible product family.
