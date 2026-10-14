"""
Kaelen Vane's Autonomous 3D & Spatial Elevation Engine
Transforms amateur, unlit, plastic 3D scenes into photorealistic, award-winning spatial masterworks.
"""

import os
import re
from typing import Dict, Any, List


class KaelenElevationEngine:
    """Kaelen Vane's 3D & Spatial Elevation Engine."""

    STUDIO_LIGHTING_RIG = """
    // 🧊 Kaelen Vane Signature Studio 3-Point PBR Lighting Rig
    const setupKaelenStudioLighting = (scene, renderer) => {
        // 1. Calibrated Tone Mapping & Soft Shadow Engine
        if (renderer) {
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            renderer.toneMappingExposure = 1.1;
            if ('outputColorSpace' in renderer) {
                renderer.outputColorSpace = THREE.SRGBColorSpace;
            } else {
                renderer.outputEncoding = THREE.sRGBEncoding;
            }
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        }

        // 2. Key Light (Primary Illumination & Soft Contact Shadows)
        const keyLight = new THREE.DirectionalLight(0xffffff, 2.5);
        keyLight.position.set(5, 8, 5);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 2048;
        keyLight.shadow.mapSize.height = 2048;
        keyLight.shadow.bias = -0.0001;
        keyLight.shadow.camera.near = 0.5;
        keyLight.shadow.camera.far = 25;
        scene.add(keyLight);

        // 3. Fill Light (Soft Cool Ambient Bounce)
        const fillLight = new THREE.DirectionalLight(0x7000ff, 1.2);
        fillLight.position.set(-5, 3, -2);
        scene.add(fillLight);

        // 4. Rim / Kicker Light (High-Contrast Silhouette Separation)
        const rimLight = new THREE.DirectionalLight(0x00f0ff, 1.8);
        rimLight.position.set(0, -4, -6);
        scene.add(rimLight);

        // 5. Ambient Radiance
        const ambientRadiance = new THREE.AmbientLight(0xffffff, 0.35);
        scene.add(ambientRadiance);
    };
    """

    def elevate(self, file_path: str) -> str:
        """Applies Kaelen's signature 3D elevation to the target file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        elevated = content

        # 1. Upgrade flat unlit materials to PBR MeshStandardMaterial
        elevated = re.sub(
            r"new\s+THREE\.MeshBasicMaterial\s*\(\s*\{([^}]*)\}\s*\)",
            r"new THREE.MeshStandardMaterial({ \1, roughness: 0.35, metalness: 0.25 })",
            elevated
        )
        elevated = re.sub(
            r"new\s+THREE\.MeshLambertMaterial\s*\(\s*\{([^}]*)\}\s*\)",
            r"new THREE.MeshStandardMaterial({ \1, roughness: 0.4, metalness: 0.15 })",
            elevated
        )

        # 2. Inject Tone Mapping & Shadow Configuration if renderer is defined
        if "new THREE.WebGLRenderer" in elevated and "ACESFilmicToneMapping" not in elevated:
            elevated = re.sub(
                r"(const\s+renderer\s*=\s*new\s+THREE\.WebGLRenderer[^\n;]+;?)",
                r"\1\n    renderer.toneMapping = THREE.ACESFilmicToneMapping;\n    renderer.toneMappingExposure = 1.1;\n    renderer.outputColorSpace = THREE.SRGBColorSpace;\n    renderer.shadowMap.enabled = true;\n    renderer.shadowMap.type = THREE.PCFSoftShadowMap;",
                elevated
            )

        # 3. Inject Studio Lighting Rig if lighting is deficient
        if "setupKaelenStudioLighting" not in elevated:
            if "<script>" in elevated:
                elevated = elevated.replace("<script>", f"<script>\n{self.STUDIO_LIGHTING_RIG}\n")
            else:
                elevated = self.STUDIO_LIGHTING_RIG + "\n" + elevated

            # Call setupKaelenStudioLighting(scene, renderer) if scene exists
            if "setupKaelenStudioLighting(scene, renderer)" not in elevated and "const scene = new THREE.Scene" in elevated:
                elevated = re.sub(
                    r"(const\s+scene\s*=\s*new\s+THREE\.Scene[^\n;]+;?)",
                    r"\1\n    setupKaelenStudioLighting(scene, renderer);",
                    elevated
                )

        # 4. Enhance OrbitControls with physical inertia / damping
        if "OrbitControls" in elevated:
            if "enableDamping" not in elevated:
                elevated = re.sub(
                    r"(const\s+controls\s*=\s*new\s+(?:THREE\.)?OrbitControls[^\n;]+;?)",
                    r"\1\n    controls.enableDamping = true;\n    controls.dampingFactor = 0.05;",
                    elevated
                )
        else:
            # If OrbitControls is completely missing from HTML, inject the CDN and instantiation
            if "</head>" in elevated and "OrbitControls.js" not in elevated:
                orbit_script = '<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>'
                elevated = elevated.replace("</head>", f"    {orbit_script}\n</head>")

            if "const camera" in elevated and "const renderer" in elevated and "const controls" not in elevated:
                elevated = re.sub(
                    r"(const\s+renderer\s*=\s*new\s+THREE\.WebGLRenderer[^\n;]+;?)",
                    r"\1\n    const controls = new THREE.OrbitControls(camera, renderer.domElement);\n    controls.enableDamping = true;\n    controls.dampingFactor = 0.05;",
                    elevated
                )

        # 5. Enable shadow casting on meshes
        elevated = re.sub(
            r"(const\s+\w+\s*=\s*new\s+THREE\.Mesh[^\n;]+;?)",
            r"\1\n    mesh.castShadow = true;\n    mesh.receiveShadow = true;",
            elevated
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(elevated)

        return elevated
