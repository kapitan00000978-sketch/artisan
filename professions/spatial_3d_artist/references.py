"""
Kaelen Vane's Empirical 3D & Spatial CGI Benchmarks
Physical, geometric, and optical standards derived from Unreal Engine 5, Blender Studio, and Apple VisionOS.
Grounds 3D evaluation in physical optics and geometric math rather than subjective opinion.
"""

from typing import Dict, Any, List


class Kaelen3DReferences:
    """Kaelen Vane's Curated Empirical 3D CGI Benchmarks."""

    BENCHMARK_PROFILES: Dict[str, Dict[str, Any]] = {
        "webgl_realtime_optimized": {
            "name": "WebGL Real-Time Interactive (Browser & Three.js 60fps)",
            "description": "Optimized real-time spatial experience with 60fps budget, PBR lighting, and inertial camera.",
            "metrics": {
                "max_poly_count": 65000,
                "max_draw_calls": 35,
                "requires_pbr_shading": True,           # MeshStandardMaterial or MeshPhysicalMaterial
                "requires_three_point_lighting": True,  # Key, Fill, Rim
                "requires_aces_tone_mapping": True,     # ACESFilmicToneMapping
                "requires_srgb_encoding": True,         # sRGBEncoding / SRGBColorSpace
                "requires_shadow_maps": True,           # PCFSoftShadowMap
                "requires_camera_damping": True,        # OrbitControls with enableDamping
                "allowed_flat_shaders": False,          # Rejects MeshBasicMaterial on hero meshes
                "target_fps": 60.0,
                "frame_time_budget_ms": 16.6
            }
        },
        "unreal_cinematic_pbr": {
            "name": "Cinematic Studio PBR (High-End Showcase)",
            "description": "Hyper-realistic studio showcase with multi-bounce lighting, contact shadows, and physical materials.",
            "metrics": {
                "max_poly_count": 250000,
                "max_draw_calls": 100,
                "requires_pbr_shading": True,
                "requires_three_point_lighting": True,
                "requires_aces_tone_mapping": True,
                "requires_srgb_encoding": True,
                "requires_shadow_maps": True,
                "requires_camera_damping": True,
                "allowed_flat_shaders": False,
                "target_fps": 60.0,
                "frame_time_budget_ms": 16.6
            }
        },
        "apple_spatial_vision": {
            "name": "Apple VisionOS Spatial Artifact",
            "description": "Pristine spatial product rendering with contact ambient occlusion, realistic glass, and fluid physics.",
            "metrics": {
                "max_poly_count": 90000,
                "max_draw_calls": 45,
                "requires_pbr_shading": True,
                "requires_three_point_lighting": True,
                "requires_aces_tone_mapping": True,
                "requires_srgb_encoding": True,
                "requires_shadow_maps": True,
                "requires_camera_damping": True,
                "allowed_flat_shaders": False,
                "target_fps": 90.0,
                "frame_time_budget_ms": 11.1
            }
        }
    }

    def __init__(self, profile_name: str = "webgl_realtime_optimized"):
        self.profile_name = profile_name
        self.active_profile = self.BENCHMARK_PROFILES.get(
            profile_name,
            self.BENCHMARK_PROFILES["webgl_realtime_optimized"]
        )

    def get_benchmarks(self) -> Dict[str, Any]:
        """Returns the active quantitative benchmark profile."""
        return self.active_profile

    def get_available_profiles(self) -> List[str]:
        """Lists all 3D benchmark profiles known to Kaelen."""
        return list(self.BENCHMARK_PROFILES.keys())
