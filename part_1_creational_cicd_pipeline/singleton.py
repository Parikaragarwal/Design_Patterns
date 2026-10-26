"""
Singleton Pattern - CI/CD Pipeline Visualizer
---------------------------------------------
Intent: Ensure a class has only one instance, and provide a global point of
access to it.
"""

import threading
from typing import Dict, Any


class PipelineConfigRegistry:
    """Thread-safe Singleton managing centralized global settings for the visualizer."""
    # Class Variables
    _instance = None
    _lock = threading.Lock()

    # Object Creation Hijacking avoiding __init__
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PipelineConfigRegistry, cls).__new__(cls)
                # Initialize default settings
                cls._instance._settings: Dict[str, Any] = {
                    "max_parallel_jobs": 4,
                    "logging_level": "INFO",
                    "visualizer_theme": "Dark-Neon",
                    "auto_retry_failed_stages": True
                }
            return cls._instance

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        return dict(self._settings)
