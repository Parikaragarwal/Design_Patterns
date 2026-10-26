"""
Abstract Factory Pattern - CI/CD Pipeline Visualizer
---------------------------------------------------
Intent: Provide an interface for creating families of related or dependent
objects (JobRunner, ConfigFormatter) without specifying their concrete classes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


# --- Abstract Products ---

class JobRunner(ABC):
    """Abstract Product A: Executes jobs for a specific CI platform."""
    
    @abstractmethod
    def run_job(self, job_name: str) -> str:
        pass


class ConfigFormatter(ABC):
    """Abstract Product B: Formats configuration files for a specific CI platform."""
    
    @abstractmethod
    def format_config(self, pipeline_data: Dict[str, Any]) -> str:
        pass


# --- Concrete Products for GitHub Actions ---

class GitHubActionsRunner(JobRunner):
    def run_job(self, job_name: str) -> str:
        return f"[GitHub Actions Runner] Executing workflow job '{job_name}' on ubuntu-latest container."


class GitHubYAMLFormatter(ConfigFormatter):
    def format_config(self, pipeline_data: Dict[str, Any]) -> str:
        name = pipeline_data.get("name", "CI Pipeline")
        return f"name: {name}\non: [push, pull_request]\njobs:\n  build:\n    runs-on: ubuntu-latest"


# --- Concrete Products for GitLab CI ---

class GitLabCIRunner(JobRunner):
    def run_job(self, job_name: str) -> str:
        return f"[GitLab CI Runner] Executing pipeline job '{job_name}' using gitlab-runner docker executor."


class GitLabYAMLFormatter(ConfigFormatter):
    def format_config(self, pipeline_data: Dict[str, Any]) -> str:
        name = pipeline_data.get("name", "CI Pipeline")
        return f"# GitLab CI Config for {name}\nstages:\n  - build\n  - test\n  - deploy"


# --- Abstract Factory ---

class CIPipelineProviderFactory(ABC):
    """Abstract Factory interface declaring creation methods for families of products."""
    
    @abstractmethod
    def create_runner(self) -> JobRunner:
        pass

    @abstractmethod
    def create_formatter(self) -> ConfigFormatter:
        pass


# --- Concrete Factories ---

class GitHubActionsFactory(CIPipelineProviderFactory):
    """Concrete Factory producing GitHub Actions runner and formatter."""
    
    def create_runner(self) -> JobRunner:
        return GitHubActionsRunner()

    def create_formatter(self) -> ConfigFormatter:
        return GitHubYAMLFormatter()


class GitLabCIFactory(CIPipelineProviderFactory):
    """Concrete Factory producing GitLab CI runner and formatter."""
    
    def create_runner(self) -> JobRunner:
        return GitLabCIRunner()

    def create_formatter(self) -> ConfigFormatter:
        return GitLabYAMLFormatter()
