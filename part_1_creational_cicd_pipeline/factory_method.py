"""
Factory Method Pattern - CI/CD Pipeline Visualizer
-------------------------------------------------
Intent: Define an interface for creating a stage object, but let subclasses
decide which stage class to instantiate.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class PipelineStage(ABC):
    """Abstract Product: Represents a stage in the CI/CD pipeline."""
    
    def __init__(self, name: str):
        self.name = name
        self.status = "Pending"

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        pass


class BuildStage(PipelineStage):
    """Concrete Product A: Handles source compilation and artifact creation."""
    
    def execute(self) -> Dict[str, Any]:
        self.status = "Completed"
        return {
            "stage": self.name,
            "type": "Build",
            "status": self.status,
            "details": "Compiled source code into distribution binary artifact."
        }


class TestStage(PipelineStage):
    """Concrete Product B: Runs unit and integration test suites."""
    
    def execute(self) -> Dict[str, Any]:
        self.status = "Completed"
        return {
            "stage": self.name,
            "type": "Test",
            "status": self.status,
            "details": "Executed 42 unit tests; 100% passed."
        }


class DeployStage(PipelineStage):
    """Concrete Product C: Handles deployment to target environment."""
    
    def execute(self) -> Dict[str, Any]:
        self.status = "Completed"
        return {
            "stage": self.name,
            "type": "Deploy",
            "status": self.status,
            "details": "Deployed artifact to Kubernetes cluster namespace 'production'."
        }


# --- Creator (Factory Method) ---

class PipelineStageFactory(ABC):
    """Abstract Creator: Declares the factory method for creating stages."""
    
    @abstractmethod
    def create_stage(self, name: str) -> PipelineStage:
        pass

    def run_stage(self, name: str) -> Dict[str, Any]:
        """Convenience method that creates and executes a stage."""
        stage = self.create_stage(name)
        return stage.execute()


class BuildStageFactory(PipelineStageFactory):
    """Concrete Creator A: Produces BuildStage objects."""
    
    def create_stage(self, name: str) -> PipelineStage:
        return BuildStage(name)


class TestStageFactory(PipelineStageFactory):
    """Concrete Creator B: Produces TestStage objects."""
    
    def create_stage(self, name: str) -> PipelineStage:
        return TestStage(name)


class DeployStageFactory(PipelineStageFactory):
    """Concrete Creator C: Produces DeployStage objects."""
    
    def create_stage(self, name: str) -> PipelineStage:
        return DeployStage(name)
