# Lab Exam 2: Behavioral Design Patterns
## Domain: CI/CD Pipeline Visualizer & Execution Engine (Topic #8)

This project implements **3 core Gang of Four (GoF) Behavioral Design Patterns** in a clean, self-contained Python architecture. Designed as a real-time **CI/CD Pipeline Visualizer**, the project demonstrates how Behavioral patterns govern the assignment of responsibilities, dynamic algorithm selection, loose coupling between execution and monitoring, and encapsulated job scheduling.

---

## 📑 Table of Contents
1. [Architecture & System Design](#architecture--system-design)
2. [Design Patterns Overview Matrix](#design-patterns-overview-matrix)
3. [Deep-Dive Pattern Analysis & Implementation](#deep-dive-pattern-analysis--implementation)
   - [1. Strategy Pattern (Deployment Algorithms)](#1-strategy-pattern-deployment-algorithms)
   - [2. Observer Pattern (Progress Visualizer & Alert System)](#2-observer-pattern-progress-visualizer--alert-system)
   - [3. Command Pattern (Pipeline Stage Execution)](#3-command-pattern-pipeline-stage-execution)
4. [Architectural Synergy: How the Patterns Cooperate](#architectural-synergy-how-the-patterns-cooperate)
5. [Running the Demonstration](#running-the-demonstration)
6. [🎙️ Viva Voce & Code Walkthrough Master Guide](#️-viva-voce--code-walkthrough-master-guide)
   - [Opening Statement & Project Pitch](#opening-statement--project-pitch)
   - [Pattern-by-Pattern Viva Speaking Scripts](#pattern-by-pattern-viva-speaking-scripts)
   - [Examiner Cross-Examination FAQ](#examiner-cross-examination-faq)

---

## Architecture & System Design

```text
Lab-exam-2/
├── README.md       # Comprehensive documentation, pattern analysis & viva guide
└── main.py         # Unified implementation containing all 3 patterns & 3 demo scenarios
```

### High-Level Architecture
In this pipeline visualizer:
1. **Pipeline Stages** are encapsulated as executable **Commands** (`BuildStage`, `TestStage`, `DeployStage`).
2. The deployment behavior inside `DeployStage` is parameterized using swappable **Strategies** (`FastDeployStrategy` vs. `BlueGreenDeployStrategy`).
3. The central **Pipeline** acts as both the **Invoker** (executing commands in sequence) and the **Subject** (publishing lifecycle events to `ConsoleVisualizer` and `EmailAlertNotifier` observers).

```
                  +----------------------------------------------+
                  |                   Pipeline                   |
                  |  - Invoker (Command) / Subject (Observer)    |
                  +----------------------------------------------+
                                  |              |
           (has stages)           |              | (notifies)
                 ▼                |              ▼
       +--------------------+     |    +--------------------+
       |  <<Command>>       |     |    |  <<Observer>>      |
       |  StageCommand      |     |    |  PipelineObserver  |
       +--------------------+     |    +--------------------+
       | + execute()        |     |    | + update()         |
       +--------------------+     |    +--------------------+
         ▲        ▲        ▲      |      ▲                ▲
         |        |        |      |      |                |
     +-------+ +------+ +-------+ | +-----------+ +----------------+
     | Build | | Test | |Deploy | | |ConsoleVis | |EmailAlertNotif |
     +-------+ +------+ +-------+ | +-----------+ +----------------+
                            |     
                 (uses)     |     
                            ▼     
               +-------------------------+
               | <<Strategy>>            |
               | DeployStrategy          |
               +-------------------------+
               | + deploy(app_name): str |
               +-------------------------+
                    ▲               ▲
                    |               |
          +------------------+ +-----------------------+
          |FastDeployStrategy| |BlueGreenDeployStrategy|
          +------------------+ +-----------------------+
```

---

## Design Patterns Overview Matrix

```
+-----------------------------------------------------------------------------------------+
|                                BEHAVIORAL DESIGN PATTERNS                               |
+---------------------+-------------------------------+-----------------------------------+
| Pattern             | GoF Intent                    | Role in CI/CD Pipeline Visualizer |
+---------------------+-------------------------------+-----------------------------------+
| Strategy            | Define a family of algorithms,| Interchangeable deployment logic  |
|                     | encapsulate each one, and make| (Fast Rolling vs Blue-Green Zero  |
|                     | them swappable at runtime     | Downtime) inside DeployStage      |
+---------------------+-------------------------------+-----------------------------------+
| Observer            | Define a one-to-many          | Decouple pipeline execution from  |
|                     | dependency so when one object | terminal visualization rendering  |
|                     | changes, all dependents update| and automated email alert systems |
+---------------------+-------------------------------+-----------------------------------+
| Command             | Encapsulate a request as an   | Package individual pipeline steps |
|                     | object, letting you parameter-| (Build, Test, Deploy) as discrete,|
|                     | ize, queue, and execute them  | sequential executable units       |
+---------------------+-------------------------------+-----------------------------------+
```

---

## Deep-Dive Pattern Analysis & Implementation

### 1. Strategy Pattern (Deployment Algorithms)
- **Code Reference**: [`main.py` Lines 14-35](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L14-L35)
- **GoF Intent**: "Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it."

#### Motivation & Problem Solved
Deploying software can be done in multiple ways:
- **Fast Rolling Deployment**: Pushes code directly to existing servers with minimal overhead (ideal for dev/staging environments).
- **Blue-Green Deployment**: Deploys to an idle parallel environment ("Green"), runs verification, and swaps router traffic to guarantee zero downtime (ideal for mission-critical production).

Without the Strategy pattern, `DeployStage` would contain hardcoded conditionals:
```python
# ANTI-PATTERN: Violates Open/Closed Principle
class DeployStage:
    def execute(self, mode):
        if mode == "fast":
            # Fast deploy logic
        elif mode == "blue_green":
            # Blue-green logic
```
Adding a Canary or Kubernetes Rolling strategy would require modifying `DeployStage`. With the Strategy pattern, the algorithm is cleanly isolated behind an abstract interface.

#### Implementation Structure
- **Strategy Interface**: [`DeployStrategy`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L17-L21) with abstract method `deploy(app_name: str) -> str`.
- **Concrete Strategies**:
  - [`FastDeployStrategy`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L24-L28): Returns `"Fast deployed '{app_name}' directly to servers."`
  - [`BlueGreenDeployStrategy`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L30-L34): Returns `"Deployed '{app_name}' to Green environment and switched router traffic."`
- **Context**: [`DeployStage`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L96-L106) maintains a reference to a `DeployStrategy`. Its strategy can be swapped at runtime via direct property assignment (`deploy_stage.strategy = BlueGreenDeployStrategy()`).

---

### 2. Observer Pattern (Pipeline Monitoring & Alerts)
- **Code Reference**: [`main.py` Lines 37-60, 112-139](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L37-L60)
- **GoF Intent**: "Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically."

#### Motivation & Problem Solved
When a pipeline runs, different external systems care about its progress:
1. An on-screen **Terminal Visualizer** wants to render ASCII progress symbols (`✔`, `⚙`, `✖`).
2. An **Alerting System** needs to send an emergency email or Slack alert whenever a stage fails.
3. In future extensions, an analytics database might record execution timestamps.

Hardcoding print statements and email dispatchers directly inside `Pipeline.run()` tightly couples pipeline orchestration to presentation and notifications (violating the Single Responsibility Principle). The Observer pattern establishes a clean publish-subscribe contract.

#### Implementation Structure
- **Observer Interface**: [`PipelineObserver`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L40-L44) defining `update(stage_name: str, status: str, message: str) -> None`.
- **Concrete Observers**:
  - [`ConsoleVisualizer`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L47-L52): Formats real-time visual progress indicators:
    ```text
    [Visualizer] [⚙] Build        ──> RUNNING  | In progress...
    [Visualizer] [✔] Build        ──> SUCCESS  | Code compiled and Docker image built.
    ```
  - [`EmailAlertNotifier`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L54-L59): Filters on `status == "FAILED"` and fires an alert:
    ```text
    [ALERT] 🚨 Sending urgent email: Stage 'Test' failed! Reason: 2 unit tests failed in test_auth.py.
    ```
- **Subject**: [`Pipeline`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L112-L139) maintains `observers: List[PipelineObserver]`. It provides `attach_observer()` and invokes `notify()` at every state transition.

---

### 3. Command Pattern (Pipeline Stages)
- **Code Reference**: [`main.py` Lines 62-107, 112-139](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L62-L107)
- **GoF Intent**: "Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations."

#### Motivation & Problem Solved
A CI/CD pipeline consists of multiple discrete phases: checking out code, compiling, running test suites, and deploying. Treating stages as plain method calls inside a monolithic class makes it impossible to:
- Dynamically assemble arbitrary combinations of stages.
- Reorder or inject custom stages at runtime.
- Halt pipeline execution early if any stage returns a failure.

The Command pattern turns each execution step into a standalone object implementing a uniform interface (`execute()`).

#### Implementation Structure
- **Command Interface**: [`StageCommand`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L65-L73) with `execute() -> tuple[str, str]` (returning `(status, message)`).
- **Concrete Commands**:
  - [`BuildStage`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L76-L83): Simulates artifact compilation.
  - [`TestStage`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L85-L94): Simulates test suite execution; supports `fail_tests=True` to trigger failure flows.
  - [`DeployStage`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L96-L106): Executes deployment using its configured Strategy.
- **Invoker**: [`Pipeline`](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L112-L139) stores `stages: List[StageCommand]`. In `Pipeline.run()`, it iterates over each command, executes it, checks the return status, and stops execution if `"FAILED"`.

---

## Architectural Synergy: How the Patterns Cooperate

This project demonstrates the natural intersection of behavioral patterns:

```
+-------------------------------------------------------------------------------------------+
|                                    COOPERATIVE ARCHITECTURE                               |
+-------------------------------------------------------------------------------------------+
| 1. Dual Role of Pipeline:                                                                 |
|    - Acts as the INVOKER in the Command Pattern (stores and executes StageCommands).     |
|    - Acts as the SUBJECT in the Observer Pattern (notifies attached PipelineObservers).   |
|                                                                                           |
| 2. Composition of Command & Strategy:                                                     |
|    - DeployStage is a concrete COMMAND (implements StageCommand.execute()).               |
|    - Inside its execute() method, it acts as the CONTEXT for the DeployStrategy.         |
|    - This allows runtime swapping of algorithms INSIDE an encapsulated executable command!|
+-------------------------------------------------------------------------------------------+
```

---

## Running the Demonstration

Execute the demonstration script directly:

```bash
python3 Lab-exam-2/main.py
```

### Walkthrough of Demo Execution Scenarios

The main script tests three distinct real-world execution paths:

#### Scenario 1: Successful Pipeline with Fast Deploy
- **Setup**: `BuildStage` -> `TestStage(fail_tests=False)` -> `DeployStage(FastDeployStrategy())`.
- **Output**:
  ```text
  ================ Running Pipeline: Production Release (Fast Deploy) ================
    [Visualizer] [⚙] Build        ──> RUNNING  | In progress...
    [Visualizer] [✔] Build        ──> SUCCESS  | Code compiled and Docker image built.
    [Visualizer] [⚙] Test         ──> RUNNING  | In progress...
    [Visualizer] [✔] Test         ──> SUCCESS  | All 15 unit tests passed successfully.
    [Visualizer] [⚙] Deploy       ──> RUNNING  | In progress...
    [Visualizer] [✔] Deploy       ──> SUCCESS  | Fast deployed 'MyWebApp' directly to servers.
  ================ Pipeline Run Finished ================
  ```
- **Proof**: Demonstrates smooth sequential Command execution and Observer updates.

#### Scenario 2: Pipeline Failure & Automated Alert
- **Setup**: `BuildStage` -> `TestStage(fail_tests=True)` -> `DeployStage(BlueGreenDeployStrategy())`.
- **Output**:
  ```text
  ================ Running Pipeline: Feature Branch Build (Failing Tests) ================
    [Visualizer] [⚙] Build        ──> RUNNING  | In progress...
    [Visualizer] [✔] Build        ──> SUCCESS  | Code compiled and Docker image built.
    [Visualizer] [⚙] Test         ──> RUNNING  | In progress...
    [Visualizer] [✖] Test         ──> FAILED   | 2 unit tests failed in test_auth.py.
    [ALERT] 🚨 Sending urgent email: Stage 'Test' failed! Reason: 2 unit tests failed in test_auth.py.
  Pipeline stopped due to stage failure!
  ================ Pipeline Run Finished ================
  ```
- **Proof**: Demonstrates short-circuiting execution on failure and reactive `EmailAlertNotifier` triggering without hardcoded dependencies in `Pipeline`.

#### Scenario 3: Runtime Strategy Swapping
- **Setup**: Creates a single `DeployStage` instance, executes it with `FastDeployStrategy`, dynamically assigns `deploy_stage.strategy = BlueGreenDeployStrategy()`, and re-executes.
- **Output**:
  ```text
  --- Demonstrating Strategy Pattern (Swapping Deployment Algorithm) ---
  Strategy 1: Fast deployed 'BillingService' directly to servers.
  Strategy 2: Deployed 'BillingService' to Green environment and switched router traffic.
  ```
- **Proof**: Confirms true runtime polymorphism where the deployment algorithm changes on the fly without recreating the command.

---

## 🎙️ Viva Voce & Code Walkthrough Master Guide

Use this section when presenting this folder to an external examiner.

### Opening Statement & Project Pitch
> *"Good morning, examiner. In Lab Exam 2, I have developed a CI/CD Pipeline Visualizer demonstrating three fundamental GoF Behavioral Design Patterns: Strategy, Observer, and Command. Behavioral patterns focus on communication and responsibility assignment between objects. In this system, each pipeline stage is encapsulated as an executable Command, the deployment algorithm inside the deploy stage is isolated using the Strategy pattern, and the pipeline execution is observed in real-time by decoupled visualizers and alerting services using the Observer pattern."*

---

### Pattern-by-Pattern Viva Speaking Scripts

#### 1. Explaining the Command Pattern ([`main.py` Lines 62-107](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L62-L107))
- **What to say while showing the screen**:
  > *"Sir/Ma'am, looking at lines 65 to 107 of `main.py`, I have implemented the Command pattern. The abstract class `StageCommand` declares the `execute()` method, returning a status and details tuple. We have concrete commands: `BuildStage`, `TestStage`, and `DeployStage`. The `Pipeline` class on line 112 acts as the Invoker. It maintains a list of `StageCommand` objects in `self.stages`. When `pipeline.run()` is invoked, it iterates over these commands sequentially. If any stage returns 'FAILED', the pipeline cleanly short-circuits and stops. This decouples the invocation of pipeline steps from their actual operational logic."*

#### 2. Explaining the Observer Pattern ([`main.py` Lines 37-60, 112-139](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L37-L60))
- **What to say while showing the screen**:
  > *"Next, in lines 37 to 60, we have the Observer pattern. `PipelineObserver` is an abstract subscriber interface defining the `update()` method. We have two distinct observers: `ConsoleVisualizer`, which renders live progress symbols (`✔`, `⚙`, `✖`), and `EmailAlertNotifier`, which listens for failures and triggers high-priority alerts. The `Pipeline` class serves as the Subject. In `pipeline.run()`, whenever a stage transitions to RUNNING, SUCCESS, or FAILED, it calls `self.notify()`. Crucially, `Pipeline` knows nothing about console formatting or email protocols; it simply notifies attached observers, adhering strictly to the Single Responsibility Principle."*

#### 3. Explaining the Strategy Pattern ([`main.py` Lines 14-35, 96-106](file:///home/parikar/DP-LabTest/Lab-exam-2/main.py#L14-L35))
- **What to say while showing the screen**:
  > *"In lines 14 to 35, I implemented the Strategy pattern to manage different deployment mechanisms. `DeployStrategy` defines the common `deploy()` contract. We provide two interchangeable concrete strategies: `FastDeployStrategy` for rolling updates and `BlueGreenDeployStrategy` for zero-downtime production deployment. In `DeployStage` (line 96), we inject the strategy via dependency injection. In our demonstration at line 172, we show that we can swap `deploy_stage.strategy` from Fast Deploy to Blue-Green at runtime without altering the `DeployStage` class or restarting the application."*

#### 4. Explaining the Architectural Synergy
- **What to say to impress the examiner**:
  > *"One key highlight of this architecture is how the patterns intersect. `Pipeline` has a dual identity: it is the **Invoker** in the Command pattern and simultaneously the **Subject** in the Observer pattern. Furthermore, `DeployStage` is simultaneously a **Command** to the pipeline and a **Context** for the Strategy pattern. This demonstrates real-world software engineering where design patterns complement each other rather than existing in isolation."*

---

### Examiner Cross-Examination FAQ

#### Q1: What is the key conceptual difference between the Command pattern and the Strategy pattern?
**Answer**:
- **Command Pattern** encapsulates **what to do** (an entire operation, action, or request) into an object. It represents an executable task with its parameters, which can be queued, logged, scheduled, or undone.
- **Strategy Pattern** encapsulates **how to do it** (an algorithm or business rule). It defines interchangeable ways to accomplish a specific sub-task within a context.
- In our project, `DeployStage` is the *Command* (the task to execute), while `DeployStrategy` is the *Strategy* (the specific algorithmic way deployment is carried out).

#### Q2: In your Observer pattern, is this a "Push" or "Pull" model?
**Answer**:
Our implementation uses the **Push model**. When `Pipeline.notify()` is triggered, it directly packages the `stage_name`, `status`, and `message` as arguments and pushes them to `observer.update(stage_name, status, message)`. In a Pull model, the observer would only receive a reference to the Subject and query the Subject's getters for the relevant state. The Push model was chosen here because the event payload is lightweight and universally needed by all observers.

#### Q3: How does your implementation uphold the Open/Closed Principle (OCP)?
**Answer**:
1. **Strategy**: To add a new deployment method (e.g., `CanaryDeployStrategy`), we create a new class implementing `DeployStrategy` without modifying `DeployStage` or `Pipeline`.
2. **Observer**: To add a new notification sink (e.g., `SlackAlertNotifier`), we create a class implementing `PipelineObserver` and attach it to `pipeline.attach_observer()` without touching `Pipeline` code.
3. **Command**: To add a new pipeline step (e.g., `SecurityScanStage`), we create a class inheriting from `StageCommand` and add it via `pipeline.add_stage()`.

#### Q4: What would happen if a stage failed without the Command pattern?
**Answer**:
In procedural code, stage steps are tightly coupled inside nested functions or sequentially hardcoded lines. Error handling would require complex nested `try-except` blocks or boolean flags, making it difficult to stop early, retry a stage, or log execution history. With Command objects, the invoker simply checks `status == "FAILED"` after calling `stage.execute()` and can immediately break or trigger recovery hooks cleanly.
