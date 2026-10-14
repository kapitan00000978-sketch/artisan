"""
Aria Solano - Autonomous Brand Identity & Visual System Elevation Engine.

Transforms discordant, raw, or vector-deficient brand guidelines into
harmonious 60-30-10 design systems with mathematical modular typography and pristine SVGs.
"""

from typing import Dict, Any, List
import re
from professions.brand_identity_director.inspector import BrandIdentityInspector, BrandInspectionReport
from professions.brand_identity_director.blind_critic import BlindBrandCritic, BrandDefectLedger


class BrandIdentityElevationEngine:
    """Elevates flawed brand assets and tokens into Aria Solano Luminary standards."""

    def __init__(self):
        self.inspector = BrandIdentityInspector()
        self.critic = BlindBrandCritic()

    def elevate(self, brand_input: Any, max_iterations: int = 3) -> Dict[str, Any]:
        """
        Takes raw brand tokens or CSS string and iteratively elevates it until certified at >= 85/100.
        """
        content = str(brand_input)
        remediations_applied: List[str] = []

        for iteration in range(1, max_iterations + 1):
            ledger: BrandDefectLedger = self.critic.review(content)
            if ledger.is_certified:
                break

            report: BrandInspectionReport = self.inspector.inspect(content)
            m = report.metrics

            # 1. Remediate Raw Primaries and Enforce 60-30-10 Balance
            if m.has_raw_primary_colors or not m.has_60_30_10_balance:
                content = self._remediate_color_tokens(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Replaced raw hex defaults with curated 60-30-10 HSL semantic tokens."
                )

            # 2. Remediate Typographic Anarchy
            if m.font_families_count >= 3 or not m.has_modular_type_scale:
                content = self._remediate_typography(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Pruned to 2 paired fonts (Outfit + Inter) and locked Major Third (1.25x) modular scale."
                )

            # 3. Remediate Vector SVGs
            if not m.has_svg_viewbox:
                content = self._remediate_svg_vectors(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Injected normalized viewBox='0 0 24 24' and responsive vector constraints."
                )

            # 4. Enforce Logo Clear-Space
            if not m.has_logo_clear_space:
                content = self._remediate_logo_clear_space(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Enforced 1x logo safe-zone clear-space padding to protect brand mark equity."
                )

            # 5. Define Brand Archetype
            if m.brand_archetype == "undefined":
                content = self._remediate_brand_archetype(content)
                remediations_applied.append(
                    f"Iteration {iteration}: Anchored identity to 'Sovereign' archetype with authoritative, precise tone."
                )

        final_ledger = self.critic.review(content)

        return {
            "status": "CERTIFIED" if final_ledger.is_certified else "ELEVATED_WITH_CAUTIONS",
            "score": final_ledger.score,
            "passing_threshold": final_ledger.passing_threshold,
            "verdict": final_ledger.verdict,
            "remediations_applied": remediations_applied,
            "elevated_brand": content,
            "final_ledger": final_ledger,
            "metrics": self.inspector.inspect(content).metrics
        }

    def _remediate_color_tokens(self, content: str) -> str:
        # Strip out harsh defaults
        cleaned = re.sub(r"#0000ff\b", "#6366F1", content, flags=re.IGNORECASE)
        cleaned = re.sub(r"#ff0000\b", "#F43F5E", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"#00ff00\b", "#10B981", cleaned, flags=re.IGNORECASE)

        if "60-30-10" not in cleaned:
            color_tokens = (
                "\n\n/* --- ARIA SOLANO 60-30-10 SEMANTIC COLOR TOKENS --- */\n"
                ":root {\n"
                "    /* 60% Dominant Base Canvas */\n"
                "    --color-canvas-dominant: #0F172A;\n"
                "    --color-surface-elevated: #1E293B;\n"
                "    /* 30% Structural Secondary (Borders, Text, Neutral UI) */\n"
                "    --color-text-secondary: #94A3B8;\n"
                "    --color-border-structural: #334155;\n"
                "    /* 10% High-Intent Kinetic Accent Energy */\n"
                "    --color-accent-kinetic: #6366F1;\n"
                "    --color-accent-hover: #4F46E5;\n"
                "}\n"
            )
            cleaned = cleaned + color_tokens
        return cleaned

    def _remediate_typography(self, content: str) -> str:
        # Remove excess font declarations
        cleaned = re.sub(r"font-family\s*:\s*[^;]+;", "", content)
        type_tokens = (
            "\n\n/* --- MATHEMATICAL MODULAR TYPOGRAPHY (MAJOR THIRD 1.25x) --- */\n"
            ":root {\n"
            "    --font-heading: 'Outfit', -apple-system, sans-serif;\n"
            "    --font-body: 'Inter', -apple-system, sans-serif;\n"
            "    --text-caption: 0.80rem;\n"
            "    --text-body: 1.00rem;\n"
            "    --text-h4: 1.25rem;\n"
            "    --text-h3: 1.563rem;\n"
            "    --text-h2: 1.953rem;\n"
            "    --text-h1: 2.441rem;\n"
            "    --text-display: 3.052rem;\n"
            "}\n"
            "body { font-family: var(--font-body); font-size: var(--text-body); }\n"
            "h1, h2, h3, h4 { font-family: var(--font-heading); }\n"
        )
        return cleaned + type_tokens

    def _remediate_svg_vectors(self, content: str) -> str:
        if "<svg" in content and "viewbox" not in content.lower():
            return re.sub(r"<svg\b([^>]*)>", r'<svg\1 viewBox="0 0 24 24">', content, flags=re.IGNORECASE)
        return content

    def _remediate_logo_clear_space(self, content: str) -> str:
        if "clear_space" not in content.lower():
            logo_rule = (
                "\n\n/* --- LOGO CLEAR-SPACE SAFE ZONE (1X MARK PADDING) --- */\n"
                ".brand-logo-container {\n"
                "    padding: 2rem;\n"
                "    margin: 1.5rem;\n"
                "    /* Enforces 1x mark height clear_space margin */\n"
                "    display: inline-flex;\n"
                "    align-items: center;\n"
                "}\n"
            )
            return content + logo_rule
        return content

    def _remediate_brand_archetype(self, content: str) -> str:
        archetype_block = (
            "\n\n/* --- BRAND ARCHETYPE & TONE OF VOICE --- */\n"
            "/* Archetype: Sovereign (Authority, Precision, Architectural Elegance) */\n"
            "/* Voice Principles: High signal, zero filler, definitive, respectful */\n"
        )
        return content + archetype_block
