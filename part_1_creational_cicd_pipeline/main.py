"""
Part 1: Creational Design Patterns Demonstration
Topic: CI/CD Pipeline Visualizer
------------------------------------------------
Demonstrates:
1. Factory Method Pattern
2. Abstract Factory Pattern
3. Builder Pattern
4. Singleton Pattern
5. Prototype Pattern
"""

from factory_method import BuildStageFactory, TestStageFactory, DeployStageFactory
from abstract_factory import GitHubActionsFactory, GitLabCIFactory
from builder import PipelineBuilder, PipelineDirector
from singleton import PipelineConfigRegistry
from prototype import PythonServiceTemplate, DockerServiceTemplate


def print_banner(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_factory_method():
    print_banner("1. FACTORY METHOD PATTERN")
    print("Creating and executing stages using stage factories...\n")
    
    factories = [
        ("Compilation Step", BuildStageFactory()),
        ("Automated Tests Step", TestStageFactory()),
        ("Deployment Step", DeployStageFactory())
    ]
    
    for name, factory in factories:
        result = factory.run_stage(name)
        print(f"-> Created Stage [{result['type']}]: {result['stage']}")
        print(f"   Status:  {result['status']}")
        print(f"   Details: {result['details']}\n")


def demo_abstract_factory():
    print_banner("2. ABSTRACT FACTORY PATTERN")
    print("Creating platform-specific pipeline runners & formatters...\n")

    sample_pipeline_data = {"name": "Payment Microservice CI"}

    for provider_name, factory in [("GitHub Actions", GitHubActionsFactory()), ("GitLab CI", GitLabCIFactory())]:
        runner = factory.create_runner()
        formatter = factory.create_formatter()
        
        print(f"[{provider_name} Provider Family]")
        print(f"   Runner:    {runner.run_job('Integration Test Job')}")
        print(f"   Config preview:\n" + "\n".join(f"     | {line}" for line in formatter.format_config(sample_pipeline_data).splitlines()))
        print()


def demo_builder():
    print_banner("3. BUILDER PATTERN")
    print("Constructing custom pipelines step-by-step using Director...\n")
    
    builder = PipelineBuilder()
    director = PipelineDirector(builder)
    
    pipeline_a = director.build_standard_microservice_pipeline("Auth Service Pipeline")
    pipeline_b = director.build_fast_ci_pipeline("Quick PR Checker")
    
    print(f"Pipeline A: {pipeline_a}")
    print(f"   Summary: {pipeline_a.summary()}\n")
    print(f"Pipeline B: {pipeline_b}")
    print(f"   Summary: {pipeline_b.summary()}\n")


def demo_singleton():
    print_banner("4. SINGLETON PATTERN")
    print("Accessing globally shared PipelineConfigRegistry instance...\n")
    
    reg1 = PipelineConfigRegistry()
    reg2 = PipelineConfigRegistry()
    
    print(f"Are reg1 and reg2 the exact same instance? {'YES' if reg1 is reg2 else 'NO'}")
    print(f"Initial Config: {reg1.get_all()}")
    
    print("\nModifying configuration via reg1...")
    reg1.set("max_parallel_jobs", 8)
    reg1.set("logging_level", "DEBUG")
    
    print(f"Updated Config retrieved from reg2: {reg2.get_all()}\n")


def demo_prototype():
    print_banner("5. PROTOTYPE PATTERN")
    print("Cloning and customizing pipeline templates...\n")
    
    python_proto = PythonServiceTemplate()
    cloned_pipeline = python_proto.clone()
    
    # Customizing the cloned instance without affecting prototype
    cloned_pipeline.template_name = "Customized User-Service Pipeline"
    cloned_pipeline.stages.append("SonarQube Code Analysis")
    cloned_pipeline.env_vars["CUSTOM_FLAG"] = "ENABLED"
    
    print(f"Original Prototype: {python_proto.to_dict()}")
    print(f"Cloned & Modified:  {cloned_pipeline.to_dict()}\n")


def main():
    print("============================================================")
    print("   CI/CD PIPELINE VISUALIZER - CREATIONAL PATTERNS DEMO")
    print("============================================================")
    
    demo_factory_method()
    demo_abstract_factory()
    demo_builder()
    demo_singleton()
    demo_prototype()
    
    print_banner("ALL 5 CREATIONAL PATTERNS EXECUTED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
