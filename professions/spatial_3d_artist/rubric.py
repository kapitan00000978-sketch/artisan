"""
Kaelen Vane's Weighted 3D & Spatial CGI Rubric
Mathematical, uncompromising evaluation of optical physics, PBR materials, studio lighting, and geometry efficiency.
"""

from typing import Dict, Any, List, Optional


class Kaelen3DRubric:
    """Kaelen Vane's 100-point weighted 3D CGI evaluation rubric."""

    DIMENSIONS: Dict[str, Dict[str, Any]] = {
        "pbr_material_depth": {
            "title": "PBR Material Depth & Optics",
            "weight": 0.25,
            "benchmark": "Physically-Based Shaders (MeshStandard/Physical) with roughness & metalness; zero flat unlit shaders."
        },
        "studio_lighting_shadows": {
            "title": "Studio 3-Point Lighting & Shadow Coherence",
            "weight": 0.25,
            "benchmark": "Calibrated 3-point setup (Key, Fill, Rim) with PCF soft shadow maps enabled."
        },
        "color_tone_mapping": {
            "title": "Color Calibration & ACES Filmic Tone Mapping",
            "weight": 0.20,
            "benchmark": "ACESFilmicToneMapping and sRGB color space transfer to prevent highlight clipping."
        },
        "spatial_ergonomics_camera": {
            "title": "Spatial Camera Ergonomics & Inertial Damping",
            "weight": 0.15,
            "benchmark": "Smooth OrbitControls with physical damping (enableDamping = true) for tactile spatial navigation."
        },
        "topology_performance_budget": {
            "title": "Geometric Topology & Real-Time Poly Budget",
            "weight": 0.15,
            "benchmark": "Polygon count within real-time budget (<65,000 for web real-time) with manifold normals."
        }
    }

    def evaluate(self, metrics: Dict[str, Any], benchmark_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates itemized and composite 3D CGI score out of 100."""
        target_metrics = benchmark_profile.get("metrics", {}) if benchmark_profile else {}
        max_poly = target_metrics.get("max_poly_count", 65000)

        scores: Dict[str, Any] = {}

        # 1. PBR Material Depth (0-10)
        has_pbr = metrics.get("has_pbr_materials", False)
        has_flat = metrics.get("has_flat_unlit_materials", False)

        if has_pbr and not has_flat:
            pbr_score = 10.0
        elif has_pbr and has_flat:
            pbr_score = 7.0
        elif not has_pbr and has_flat:
            pbr_score = 2.0
        else:
            pbr_score = 4.0

        scores["pbr_material_depth"] = {
            "score": pbr_score,
            "measured": "PBR Standard/Physical Shaders certified" if (has_pbr and not has_flat) else ("Mixed PBR & Flat shaders" if has_pbr else "Amateur flat unlit shaders detected"),
            "benchmark": "100% PBR Physically Based Shaders",
            "status": "PASS" if pbr_score >= 8.0 else "FAIL"
        }

        # 2. Studio Lighting & Shadows (0-10)
        has_3point = metrics.get("has_three_point_lighting", False)
        has_shadows = metrics.get("has_shadow_maps", False)
        has_soft = metrics.get("has_soft_shadows", False)
        light_count = metrics.get("light_count", 0)

        if has_3point and has_shadows and has_soft:
            light_score = 10.0
        elif has_3point and has_shadows:
            light_score = 8.5
        elif light_count >= 2:
            light_score = 6.0
        elif light_count == 1:
            light_score = 3.5
        else:
            light_score = 1.0

        scores["studio_lighting_shadows"] = {
            "score": light_score,
            "measured": f"{light_count} lights (3-Point: {has_3point}, Soft Shadows: {has_soft})",
            "benchmark": "Key + Fill + Rim Studio 3-Point Lighting + PCF Soft Shadows",
            "status": "PASS" if light_score >= 8.5 else "FAIL"
        }

        # 3. Color Calibration & Tone Mapping (0-10)
        has_aces = metrics.get("has_aces_tone_mapping", False)
        has_srgb = metrics.get("has_srgb_encoding", False)

        if has_aces and has_srgb:
            color_score = 10.0
        elif has_aces or has_srgb:
            color_score = 7.0
        else:
            color_score = 2.5

        scores["color_tone_mapping"] = {
            "score": color_score,
            "measured": "ACES Filmic + sRGB calibrated" if (has_aces and has_srgb) else ("Partial color calibration" if (has_aces or has_srgb) else "Raw uncalibrated linear rendering"),
            "benchmark": "ACESFilmicToneMapping + sRGB color transfer",
            "status": "PASS" if color_score >= 8.0 else "FAIL"
        }

        # 4. Spatial Camera Ergonomics & Inertial Damping (0-10)
        has_orbit = metrics.get("has_orbit_controls", False)
        has_damping = metrics.get("has_camera_damping", False)

        if has_orbit and has_damping:
            cam_score = 10.0
        elif has_orbit:
            cam_score = 7.5
        else:
            cam_score = 3.0

        scores["spatial_ergonomics_camera"] = {
            "score": cam_score,
            "measured": "Inertial OrbitControls with physical damping" if (has_orbit and has_damping) else ("Basic static OrbitControls" if has_orbit else "Fixed non-interactive camera"),
            "benchmark": "OrbitControls with enableDamping = true",
            "status": "PASS" if cam_score >= 8.0 else "FAIL"
        }

        # 5. Geometric Topology & Poly Budget (0-10)
        poly_count = metrics.get("estimated_poly_count", 0)
        manifold = metrics.get("manifold_topology", True)

        if poly_count <= max_poly and manifold:
            topo_score = 10.0
        elif poly_count <= max_poly * 1.5 and manifold:
            topo_score = 8.0
        elif poly_count <= max_poly * 3.0:
            topo_score = 5.0
        else:
            topo_score = 3.0

        scores["topology_performance_budget"] = {
            "score": topo_score,
            "measured": f"{poly_count:,} triangles (Manifold: {manifold})",
            "benchmark": f"<= {max_poly:,} triangles",
            "status": "PASS" if topo_score >= 8.0 else "FAIL"
        }

        # Composite score calculation
        total_score = round(sum(
            scores[dim]["score"] * self.DIMENSIONS[dim]["weight"]
            for dim in self.DIMENSIONS
        ) * 10, 1)

        return {
            "evaluator": "Kaelen Vane (Principal 3D & Spatial CGI Artist)",
            "total_score": total_score,
            "passing_threshold": 85.0,
            "passed": total_score >= 85.0,
            "dimensions": scores
        }
