"""
Prototype Pattern - CI/CD Pipeline Visualizer
---------------------------------------------
Intent: Specify the kinds of objects to create using a prototypical instance,
and create new objects by copying this prototype.
"""

import copy
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class PipelineTemplate(ABC):
    """Abstract Prototype declaring the clone method."""
    
    def __init__(self, template_name: str, stages: List[str], env_vars: Dict[str, str]):
        self.template_name = template_name
        self.stages = list(stages)
        self.env_vars = dict(env_vars)

    @abstractmethod
    def clone(self) -> 'PipelineTemplate':
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_name": self.template_name,
            "stages": self.stages,
            "env_vars": self.env_vars
        }


class PythonServiceTemplate(PipelineTemplate):
    """Concrete Prototype for Python microservice pipelines."""
    
    def __init__(self, template_name: str = "Python Microservice Standard"):
        super().__init__(
            template_name=template_name,
            stages=["Checkout", "Pip Install Dependencies", "Pytest Suite", "Flake8 Lint", "Docker Build"],
            env_vars={"PYTHON_VERSION": "3.11", "POETRY_ENV": "production"}
        )

    def clone(self) -> 'PythonServiceTemplate':
        """Deep copy of prototype instance."""
        return copy.deepcopy(self)


class DockerServiceTemplate(PipelineTemplate):
    """Concrete Prototype for Docker containerized service pipelines."""
    
    def __init__(self, template_name: str = "Docker Container Pipeline"):
        super().__init__(
            template_name=template_name,
            stages=["Checkout", "Docker Lint", "Docker Build", "Trivy Vulnerability Scan", "Push Registry"],
            env_vars={"DOCKER_BUILDKIT": "1", "REGISTRY_URL": "docker.io/myrepo"}
        )

    def clone(self) -> 'DockerServiceTemplate':
        """Deep copy of prototype instance."""
        return copy.deepcopy(self)
