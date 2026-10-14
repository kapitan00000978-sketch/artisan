"""
Marcus Sterling's Empirical Software Architecture Benchmarks
Mathematical, structural standards derived from Clean Architecture, SOLID, and Martin Fowler's Refactoring principles.
Grounds code review in objective metrics (cyclomatic complexity, line length, type coverage, and exception discipline).
"""

from typing import Dict, Any, List


class MarcusArchitectureReferences:
    """Marcus Sterling's Curated Empirical Architecture Benchmarks."""

    BENCHMARK_PROFILES: Dict[str, Dict[str, Any]] = {
        "clean_modular_service": {
            "name": "Clean Modular Service (Production Standard)",
            "description": "Strict modular boundaries, small focused functions, typed contracts, zero debt.",
            "metrics": {
                "max_cyclomatic_complexity": 8,
                "max_function_lines": 40,
                "min_type_annotation_pct": 90.0,
                "max_allowed_stubs_or_todos": 0,
                "max_allowed_empty_catches": 0,
                "requires_pure_helpers": True,
                "forbid_global_mutation": True
            }
        },
        "enterprise_resilient_core": {
            "name": "Enterprise Resilient Core (Mission-Critical)",
            "description": "Ultra-low cyclomatic complexity, absolute zero debt, defense-in-depth error handling.",
            "metrics": {
                "max_cyclomatic_complexity": 6,
                "max_function_lines": 30,
                "min_type_annotation_pct": 100.0,
                "max_allowed_stubs_or_todos": 0,
                "max_allowed_empty_catches": 0,
                "requires_pure_helpers": True,
                "forbid_global_mutation": True
            }
        },
        "modern_fast_prototype": {
            "name": "Modern Pragmatic Prototype",
            "description": "Permits slightly longer functions while maintaining zero-crash exception discipline and zero stubs.",
            "metrics": {
                "max_cyclomatic_complexity": 12,
                "max_function_lines": 60,
                "min_type_annotation_pct": 75.0,
                "max_allowed_stubs_or_todos": 0,
                "max_allowed_empty_catches": 0,
                "requires_pure_helpers": False,
                "forbid_global_mutation": True
            }
        }
    }

    def __init__(self, profile_name: str = "clean_modular_service"):
        self.profile_name = profile_name
        self.active_profile = self.BENCHMARK_PROFILES.get(
            profile_name,
            self.BENCHMARK_PROFILES["clean_modular_service"]
        )

    def get_benchmarks(self) -> Dict[str, Any]:
        """Returns the active quantitative benchmark profile."""
        return self.active_profile

    def get_available_profiles(self) -> List[str]:
        """Lists all architectural profiles known to Marcus."""
        return list(self.BENCHMARK_PROFILES.keys())
