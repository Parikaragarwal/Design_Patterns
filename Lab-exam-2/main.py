"""CI/CD Pipeline Visualizer (Topic #8 from studentProjects.pdf)

A simple, 1-hour student project demonstrating 3 Behavioral Design Patterns:
1. Observer Pattern: Notifies visualizer and alert system on stage progress.
2. Strategy Pattern: Swappable deployment strategies (Fast Deploy vs Blue-Green).
3. Command Pattern: Encapsulates pipeline stages as executable commands.
"""

from abc import ABC, abstractmethod
from typing import List


# =====================================================================
# 1. STRATEGY PATTERN (Deployment Strategies)
# =====================================================================

class DeployStrategy(ABC):
    """Strategy interface for deploying the application."""
    @abstractmethod
    def deploy(self, app_name: str) -> str:
        pass


class FastDeployStrategy(DeployStrategy):
    """Direct rolling deployment for quick updates."""
    def deploy(self, app_name: str) -> str:
        return f"Fast deployed '{app_name}' directly to servers."


class BlueGreenDeployStrategy(DeployStrategy):
    """Zero-downtime deployment swapping traffic between two environments."""
    def deploy(self, app_name: str) -> str:
        return f"Deployed '{app_name}' to Green environment and switched router traffic."


# =====================================================================
# 2. OBSERVER PATTERN (Pipeline Monitoring & Alerts)
# =====================================================================

class PipelineObserver(ABC):
    """Observer interface to receive pipeline status updates."""
    @abstractmethod
    def update(self, stage_name: str, status: str, message: str) -> None:
        pass


class ConsoleVisualizer(PipelineObserver):
    """Visualizes the pipeline stages graphically in the console."""
    def update(self, stage_name: str, status: str, message: str) -> None:
        symbol = "✔" if status == "SUCCESS" else ("✖" if status == "FAILED" else "⚙")
        print(f"  [Visualizer] [{symbol}] {stage_name:<12} ──> {status:<8} | {message}")


class EmailAlertNotifier(PipelineObserver):
    """Sends an alert if any stage fails."""
    def update(self, stage_name: str, status: str, message: str) -> None:
        if status == "FAILED":
            print(f"  [ALERT] 🚨 Sending urgent email: Stage '{stage_name}' failed! Reason: {message}")


# =====================================================================
# 3. COMMAND PATTERN (Pipeline Stages)
# =====================================================================

class StageCommand(ABC):
    """Command interface for a pipeline stage."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self) -> tuple[str, str]:
        """Returns (status, message)."""
        pass


class BuildStage(StageCommand):
    def __init__(self):
        super().__init__("Build")

    def execute(self) -> tuple[str, str]:
        # Simulating compiling code and creating container image
        return "SUCCESS", "Code compiled and Docker image built."


class TestStage(StageCommand):
    def __init__(self, fail_tests: bool = False):
        super().__init__("Test")
        self.fail_tests = fail_tests

    def execute(self) -> tuple[str, str]:
        if self.fail_tests:
            return "FAILED", "2 unit tests failed in test_auth.py."
        return "SUCCESS", "All 15 unit tests passed successfully."


class DeployStage(StageCommand):
    def __init__(self, strategy: DeployStrategy, app_name: str = "MyWebApp"):
        super().__init__("Deploy")
        self.strategy = strategy
        self.app_name = app_name

    def execute(self) -> tuple[str, str]:
        # Uses Strategy Pattern to execute deployment
        message = self.strategy.deploy(self.app_name)
        return "SUCCESS", message


# =====================================================================
# PIPELINE RUNNER (Subject in Observer, Invoker in Command)
# =====================================================================

class Pipeline:
    """Manages and executes stages, notifying observers along the way."""
    def __init__(self, name: str):
        self.name = name
        self.stages: List[StageCommand] = []
        self.observers: List[PipelineObserver] = []

    def attach_observer(self, observer: PipelineObserver) -> None:
        self.observers.append(observer)

    def add_stage(self, stage: StageCommand) -> None:
        self.stages.append(stage)

    def notify(self, stage_name: str, status: str, message: str) -> None:
        for obs in self.observers:
            obs.update(stage_name, status, message)

    def run(self) -> None:
        print(f"\n================ Running Pipeline: {self.name} ================")
        for stage in self.stages:
            self.notify(stage.name, "RUNNING", "In progress...")
            status, msg = stage.execute()
            self.notify(stage.name, status, msg)
            if status == "FAILED":
                print("Pipeline stopped due to stage failure!")
                break
        print("================ Pipeline Run Finished ================\n")


# =====================================================================
# DEMONSTRATION / MAIN
# =====================================================================

if __name__ == "__main__":
    # Setup Observers
    visualizer = ConsoleVisualizer()
    notifier = EmailAlertNotifier()

    # --- Run 1: Successful Pipeline with Fast Deploy ---
    pipeline1 = Pipeline("Production Release (Fast Deploy)")
    pipeline1.attach_observer(visualizer)
    pipeline1.attach_observer(notifier)

    pipeline1.add_stage(BuildStage())
    pipeline1.add_stage(TestStage(fail_tests=False))
    pipeline1.add_stage(DeployStage(FastDeployStrategy()))
    pipeline1.run()

    # --- Run 2: Pipeline with Failure and Alert ---
    pipeline2 = Pipeline("Feature Branch Build (Failing Tests)")
    pipeline2.attach_observer(visualizer)
    pipeline2.attach_observer(notifier)

    pipeline2.add_stage(BuildStage())
    pipeline2.add_stage(TestStage(fail_tests=True))  # Intentionally fail
    pipeline2.add_stage(DeployStage(BlueGreenDeployStrategy()))
    pipeline2.run()

    # --- Run 3: Showing Strategy Swapping ---
    print("--- Demonstrating Strategy Pattern (Swapping Deployment Algorithm) ---")
    deploy_stage = DeployStage(FastDeployStrategy(), app_name="BillingService")
    _, msg1 = deploy_stage.execute()
    print("Strategy 1:", msg1)

    deploy_stage.strategy = BlueGreenDeployStrategy()
    _, msg2 = deploy_stage.execute()
    print("Strategy 2:", msg2)
