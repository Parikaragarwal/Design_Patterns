"""
Builder Pattern - CI/CD Pipeline Visualizer
-------------------------------------------
Intent: Separate the construction of a complex Pipeline object from its representation,
allowing the same construction process to create different pipeline configurations.
"""

from typing import List, Dict, Any


class Pipeline:
    """Complex Product: Represents a full CI/CD Pipeline configuration."""
    
    def __init__(self):
        self.name: str = "Untitled Pipeline"
        self.stages: List[str] = []
        self.environment: Dict[str, str] = {}
        self.timeout_minutes: int = 30
        self.notification_webhook: str = ""

    def summary(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "stages": self.stages,
            "environment": self.environment,
            "timeout_minutes": self.timeout_minutes,
            "webhook": self.notification_webhook or "None"
        }

    def __str__(self) -> str:
        stages_str = " -> ".join(self.stages) if self.stages else "No stages"
        return f"Pipeline('{self.name}', Stages=[{stages_str}], Timeout={self.timeout_minutes}m)"


class PipelineBuilder:
    """Builder interface & implementation for step-by-step pipeline assembly."""
    
    def __init__(self):
        self.reset()

    def reset(self) -> 'PipelineBuilder':
        self._pipeline = Pipeline()
        return self

    def set_name(self, name: str) -> 'PipelineBuilder':
        self._pipeline.name = name
        return self

    def add_stage(self, stage_name: str) -> 'PipelineBuilder':
        self._pipeline.stages.append(stage_name)
        return self

    def set_environment_variable(self, key: str, value: str) -> 'PipelineBuilder':
        self._pipeline.environment[key] = value
        return self

    def set_timeout(self, minutes: int) -> 'PipelineBuilder':
        self._pipeline.timeout_minutes = minutes
        return self

    def set_notification_webhook(self, webhook_url: str) -> 'PipelineBuilder':
        self._pipeline.notification_webhook = webhook_url
        return self

    def build(self) -> Pipeline:
        product = self._pipeline
        self.reset()
        return product


class PipelineDirector:
    """Director: Defines predefined sequences of construction steps."""
    
    def __init__(self, builder: PipelineBuilder):
        self._builder = builder

    def build_standard_microservice_pipeline(self, name: str) -> Pipeline:
        return (self._builder.reset()
                .set_name(name)
                .add_stage("Checkout Code")
                .add_stage("Compile & Unit Test")
                .add_stage("Build Docker Image")
                .add_stage("Security Vulnerability Scan")
                .add_stage("Deploy to Staging")
                .set_environment_variable("ENV", "staging")
                .set_timeout(45)
                .set_notification_webhook("https://slack.com/api/webhooks/cicd")
                .build())

    def build_fast_ci_pipeline(self, name: str) -> Pipeline:
        return (self._builder.reset()
                .set_name(name)
                .add_stage("Checkout Code")
                .add_stage("Linter & Fast Unit Test")
                .set_environment_variable("ENV", "test")
                .set_timeout(10)
                .build())
