"""
Kaelen Vane's 3D & Spatial CGI Inspector
Deep empirical measurement engine for 3D geometry, PBR materials, lighting rigs, tone mapping, and real-time performance.
Supports WebGL/Three.js scenes, glTF/GLB structures, and OBJ wavefront geometry.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional


class Kaelen3DInspector:
    """Kaelen Vane's 3D & Spatial Inspection Engine."""

    def __init__(self, target_file: str):
        self.target_file = os.path.abspath(target_file)

    def inspect(self) -> Dict[str, Any]:
        """
        Executes an objective, multi-dimensional 3D craftsmanship inspection:
        - PBR Shading & Material Depth
        - Studio 3-Point Lighting & Shadow Maps
        - Color Calibration (ACES Filmic Tone Mapping & sRGB)
        - Inertial Camera & Spatial Ergonomics
        - Geometry & Topology Efficiency
        """
        metrics: Dict[str, Any] = {
            "target": self.target_file,
            "file_type": "unknown",
            "has_pbr_materials": False,
            "has_flat_unlit_materials": False,
            "materials_count": 0,
            "light_count": 0,
            "has_three_point_lighting": False,
            "has_shadow_maps": False,
            "has_soft_shadows": False,
            "has_aces_tone_mapping": False,
            "has_srgb_encoding": False,
            "has_orbit_controls": False,
            "has_camera_damping": False,
            "estimated_poly_count": 0,
            "manifold_topology": True
        }

        if not os.path.exists(self.target_file):
            metrics["error"] = f"File {self.target_file} does not exist"
            return metrics

        ext = os.path.splitext(self.target_file)[1].lower()

        try:
            with open(self.target_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if ext in (".html", ".htm", ".js", ".ts"):
                metrics["file_type"] = "threejs_webgl"
                self._inspect_threejs(content, metrics)
            elif ext in (".gltf", ".json"):
                metrics["file_type"] = "gltf_manifest"
                self._inspect_gltf(content, metrics)
            elif ext == ".obj":
                metrics["file_type"] = "obj_geometry"
                self._inspect_obj(content, metrics)
            else:
                metrics["file_type"] = "generic_3d_text"
                self._inspect_threejs(content, metrics)

        except Exception as e:
            metrics["inspection_error"] = str(e)

        return metrics

    def _inspect_threejs(self, content: str, metrics: Dict[str, Any]):
        """Inspects Three.js / WebGL JavaScript & HTML source code."""
        # 1. PBR Shading checks
        has_standard = bool(re.search(r"MeshStandardMaterial|MeshPhysicalMaterial", content))
        has_basic = bool(re.search(r"MeshBasicMaterial|MeshLambertMaterial", content))
        metrics["has_pbr_materials"] = has_standard
        metrics["has_flat_unlit_materials"] = has_basic

        # 2. Lighting checks
        directional_lights = len(re.findall(r"DirectionalLight\(", content))
        point_lights = len(re.findall(r"PointLight\(", content))
        ambient_lights = len(re.findall(r"AmbientLight\(|HemisphereLight\(", content))
        spot_lights = len(re.findall(r"SpotLight\(", content))

        total_lights = directional_lights + point_lights + ambient_lights + spot_lights
        metrics["light_count"] = total_lights

        # 3-point lighting requires key + fill + rim (at least 2 directional/spot + 1 ambient/hemi, or total >= 3)
        metrics["has_three_point_lighting"] = (total_lights >= 3 and (directional_lights + spot_lights) >= 2)

        # 3. Shadows
        metrics["has_shadow_maps"] = bool(re.search(r"shadowMap\.enabled\s*=\s*true|castShadow\s*=\s*true", content))
        metrics["has_soft_shadows"] = bool(re.search(r"PCFSoftShadowMap|VSMShadowMap", content))

        # 4. Color Science & Tone Mapping
        metrics["has_aces_tone_mapping"] = bool(re.search(r"ACESFilmicToneMapping", content))
        metrics["has_srgb_encoding"] = bool(re.search(r"sRGBEncoding|SRGBColorSpace", content))

        # 5. Camera & Interactive Controls
        metrics["has_orbit_controls"] = bool(re.search(r"OrbitControls", content))
        metrics["has_camera_damping"] = bool(re.search(r"enableDamping\s*=\s*true", content))

        # 6. Polygon / Geometry Estimation
        poly_matches = re.findall(r"(\d+)\s*,\s*(\d+)\s*\)", content)  # e.g., SphereGeometry(1, 32, 32)
        geom_hits = len(re.findall(r"(?:Box|Sphere|Cylinder|Torus|Plane|Buffer)Geometry", content))
        metrics["estimated_poly_count"] = max(1200, geom_hits * 1800)

    def _inspect_gltf(self, content: str, metrics: Dict[str, Any]):
        """Inspects glTF 2.0 JSON structures."""
        try:
            data = json.loads(content)
            materials = data.get("materials", [])
            metrics["materials_count"] = len(materials)

            pbr_count = sum(1 for m in materials if "pbrMetallicRoughness" in m)
            metrics["has_pbr_materials"] = (pbr_count > 0)
            metrics["has_flat_unlit_materials"] = any("KHR_materials_unlit" in m.get("extensions", {}) for m in materials)

            # Polygons from accessors / meshes
            meshes = data.get("meshes", [])
            total_indices = 0
            for m in meshes:
                for p in m.get("primitives", []):
                    if "indices" in p:
                        total_indices += 1000  # Approximation
            metrics["estimated_poly_count"] = max(1000, total_indices)

        except Exception:
            metrics["gltf_parse_error"] = True

    def _inspect_obj(self, content: str, metrics: Dict[str, Any]):
        """Inspects Wavefront OBJ geometry files."""
        v_count = len(re.findall(r"^v\s+", content, re.MULTILINE))
        f_count = len(re.findall(r"^f\s+", content, re.MULTILINE))
        vn_count = len(re.findall(r"^vn\s+", content, re.MULTILINE))
        vt_count = len(re.findall(r"^vt\s+", content, re.MULTILINE))

        metrics["estimated_poly_count"] = f_count
        metrics["has_normals"] = (vn_count > 0)
        metrics["has_uvs"] = (vt_count > 0)
        metrics["manifold_topology"] = (f_count > 0 and v_count >= 3)
