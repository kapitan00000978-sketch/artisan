"""
Elena Rostova's Reference Design Benchmarks & Profiles
Empirical standards derived from world-class digital products (Linear, Stripe, Apple, Vercel).
Used by Elena to ground visual critique in mathematical metrics rather than subjective taste.
"""

from typing import Dict, Any, List


class ElenaDesignReferences:
    """Elena's Curated Empirical Design Benchmarks."""

    BENCHMARK_PROFILES: Dict[str, Dict[str, Any]] = {
        "linear_dark_luxe": {
            "name": "Linear Dark Luxe (SaaS & Developer Tools)",
            "description": "Deep space backgrounds, high-contrast crisp text, subtle specular borders, 8pt rhythm.",
            "metrics": {
                "min_contrast_ratio": 7.0,          # WCAG AAA
                "recommended_h1_size_px": 56.0,
                "recommended_body_size_px": 16.0,
                "target_scale_ratio": 3.5,          # 56 / 16
                "grid_unit_px": 8,
                "target_grid_adherence_pct": 85.0,
                "requires_liquid_glass": True,
                "requires_specular_borders": True,
                "requires_micro_interactions": True,
                "primary_font": "Inter",
                "heading_font": "Outfit",
                "background_hex": "#090b10",
                "text_hex": "#ffffff"
            }
        },
        "apple_spatial_glass": {
            "name": "Apple Spatial Vibrancy (Consumer & Luxury)",
            "description": "Frosted glassmorphism, mathematical radii, ambient diffuse shadows, fluid physics.",
            "metrics": {
                "min_contrast_ratio": 6.5,
                "recommended_h1_size_px": 48.0,
                "recommended_body_size_px": 17.0,
                "target_scale_ratio": 2.82,
                "grid_unit_px": 8,
                "target_grid_adherence_pct": 80.0,
                "requires_liquid_glass": True,
                "requires_specular_borders": True,
                "requires_micro_interactions": True,
                "primary_font": "SF Pro Text",
                "heading_font": "SF Pro Display",
                "background_hex": "#0a0a0c",
                "text_hex": "#f5f5f7"
            }
        },
        "stripe_fluid_ambient": {
            "name": "Stripe Fluid Ambient (Fintech & Commerce)",
            "description": "Dynamic radial gradients, bold clean typography, card elevation, magnetic CTAs.",
            "metrics": {
                "min_contrast_ratio": 5.5,
                "recommended_h1_size_px": 64.0,
                "recommended_body_size_px": 18.0,
                "target_scale_ratio": 3.55,
                "grid_unit_px": 8,
                "target_grid_adherence_pct": 75.0,
                "requires_liquid_glass": True,
                "requires_specular_borders": True,
                "requires_micro_interactions": True,
                "primary_font": "Inter",
                "heading_font": "Outfit",
                "background_hex": "#0a2540",
                "text_hex": "#ffffff"
            }
        }
    }

    def __init__(self, profile_name: str = "linear_dark_luxe"):
        self.profile_name = profile_name
        self.active_profile = self.BENCHMARK_PROFILES.get(
            profile_name,
            self.BENCHMARK_PROFILES["linear_dark_luxe"]
        )

    def get_benchmarks(self) -> Dict[str, Any]:
        """Returns the active quantitative benchmark profile."""
        return self.active_profile

    def get_available_profiles(self) -> List[str]:
        """Lists all benchmark design profiles known to Elena."""
        return list(self.BENCHMARK_PROFILES.keys())
