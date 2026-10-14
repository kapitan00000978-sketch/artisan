"""
Kaelen Vane's Blind 3D & Spatial Critic
The Critic NEVER looks at developer prompts or excuses.
It evaluates ONLY rendered visual outcomes, computed spatial metrics, and physical rubrics.
Produces an uncompromising 3D CGI verdict and structured defect ledger.
"""

from typing import Dict, Any, List


class KaelenBlindCritic:
    """Kaelen Vane's Blind 3D & Spatial Critic."""

    def __init__(self, passing_score: float = 85.0):
        self.passing_score = passing_score

    def critique(self, evaluation: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Audits 3D outcomes blindly and issues Kaelen's professional verdict."""
        total_score = evaluation["total_score"]
        dims = evaluation["dimensions"]
        defect_ledger: List[Dict[str, Any]] = []

        # 1. PBR Material Critique
        pbr = dims.get("pbr_material_depth", {})
        if pbr.get("status") == "FAIL":
            defect_ledger.append({
                "category": "PBR_SHADING",
                "severity": "BLOCKER",
                "flaw": f"Amateur or flat unlit shading detected ({pbr.get('measured')}). Objects look like 1998 cheap plastic.",
                "kaelen_directive": "Replace MeshBasicMaterial with MeshStandardMaterial or MeshPhysicalMaterial. Configure roughness (0.25-0.5) and metalness (0.1-0.8)."
            })

        # 2. Lighting & Shadows Critique
        lighting = dims.get("studio_lighting_shadows", {})
        if lighting.get("status") == "FAIL":
            defect_ledger.append({
                "category": "LIGHTING_AND_SHADOWS",
                "severity": "CRITICAL",
                "flaw": f"Deficient lighting setup ({lighting.get('measured')}). Lacks physical spatial illumination and depth.",
                "kaelen_directive": "Install Studio 3-Point Lighting (Key Light with soft shadow maps, Fill Light, Rim Light) plus subtle ambient radiance."
            })

        # 3. Color Calibration & Tone Mapping Critique
        tone = dims.get("color_tone_mapping", {})
        if tone.get("status") == "FAIL":
            defect_ledger.append({
                "category": "COLOR_SCIENCE",
                "severity": "MAJOR",
                "flaw": f"Uncalibrated color science ({tone.get('measured')}). Highlights risk nuclear clipping and shadows crush to mud.",
                "kaelen_directive": "Activate ACESFilmicToneMapping and sRGB transfer encoding on WebGLRenderer (outputColorSpace = THREE.SRGBColorSpace)."
            })

        # 4. Camera & Ergonomics Critique
        camera = dims.get("spatial_ergonomics_camera", {})
        if camera.get("status") == "FAIL":
            defect_ledger.append({
                "category": "SPATIAL_ERGONOMICS",
                "severity": "MAJOR",
                "flaw": f"Stiff or frozen camera mechanics ({camera.get('measured')}). Spatial navigation feels clunky.",
                "kaelen_directive": "Bind OrbitControls with physical damping (enableDamping = true, dampingFactor = 0.05) and update in render animation loop."
            })

        # 5. Topology Critique
        topo = dims.get("topology_performance_budget", {})
        if topo.get("status") == "FAIL":
            defect_ledger.append({
                "category": "TOPOLOGY_AND_BUDGET",
                "severity": "CRITICAL",
                "flaw": f"Polygon bloat or non-manifold topology ({topo.get('measured')}). Exceeds real-time frame budget.",
                "kaelen_directive": "Decimate unnecessary planar vertices, re-topologize to clean quad flow, and recalculate surface normals."
            })

        passed = (total_score >= self.passing_score) and (len([d for d in defect_ledger if d["severity"] == "BLOCKER"]) == 0)

        verdict_summary = (
            "💎 [KAELEN VERIFIED]: Masterful spatial coherence, calibrated 3-point lighting, and photorealistic PBR shading certified."
            if passed else
            "❌ [KAELEN REJECTED]: 3D asset/scene violates physical rendering laws and topology standards. Requires spatial elevation."
        )

        return {
            "critic": "Kaelen Vane (Principal 3D & Spatial CGI Artist)",
            "verdict": "CERTIFIED" if passed else "REJECTED",
            "verdict_summary": verdict_summary,
            "score": total_score,
            "passing_threshold": self.passing_score,
            "defects_count": len(defect_ledger),
            "defect_ledger": defect_ledger
        }
