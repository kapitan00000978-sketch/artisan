"""
🎨 ARIA SOLANO — GLOBAL BRAND DIRECTOR & VISUAL IDENTITY MASTER
Autonomous visual conscience, 60-30-10 color inspection, blind outcome critique,
and automated mathematical brand design system elevation engine.

Usage:
    python professions/brand_identity_director/master.py <brand_file> [--elevate]
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception as _enc_err:
        sys.stderr.write(f"Note: UTF-8 stdout reconfiguration skipped: {_enc_err}\n")

try:
    from .references import BrandReferenceLibrary
    from .inspector import BrandIdentityInspector, BrandInspectionReport
    from .rubric import BrandIdentityRubric, BrandRubricEvaluation
    from .blind_critic import BlindBrandCritic, BrandDefectLedger
    from .elevation_engine import BrandIdentityElevationEngine
except ImportError:
    from references import BrandReferenceLibrary
    from inspector import BrandIdentityInspector, BrandInspectionReport
    from rubric import BrandIdentityRubric, BrandRubricEvaluation
    from blind_critic import BlindBrandCritic, BrandDefectLedger
    from elevation_engine import BrandIdentityElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class AriaSolanoMaster:
    """
    Aria Solano: The living visual identity sovereign, design system alchemist,
    and brand conscience. Eliminates raw color defaults, enforces mathematical modular scales,
    and elevates products into indelible cultural icons.
    """

    def __init__(
        self,
        target_path: Optional[str] = None,
        passing_threshold: int = 85,
        max_cycles: int = 3
    ):
        self.target_path = os.path.abspath(target_path) if target_path else None
        self.passing_threshold = passing_threshold
        self.max_cycles = max_cycles
        self.inspector = BrandIdentityInspector()
        self.rubric = BrandIdentityRubric()
        self.critic = BlindBrandCritic()
        self.elevation_engine = BrandIdentityElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous brand audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Brand target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype brand tokens for testing or demo
            data = (
                "/* Flawed Brand Style Guide */\n"
                ":root {\n"
                "    --primary-color: #0000ff;\n"
                "    --alert-color: #ff0000;\n"
                "    font-family: 'Comic Sans';\n"
                "}\n"
                "h1 { font-family: 'Roboto'; font-size: 22px; }\n"
                "p { font-family: 'Times New Roman'; font-size: 15px; }\n"
                '<svg width="100" height="100"><circle cx="50" cy="50" r="40"/></svg>\n'
            )

        # Step 1: Initial Blind Critic Review
        ledger: BrandDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_brand"]
            ledger = elevated_result["final_ledger"]

        # Step 3: Record in Journal
        self._record_journal_entry(
            initial_score=initial_score,
            final_score=ledger.score,
            is_certified=ledger.is_certified,
            fatal_defects=ledger.fatal_defects_count,
            verdict=ledger.verdict
        )

        # Step 4: Generate Executive Briefing
        briefing = self._generate_briefing(current_data, ledger)

        return {
            "is_certified": ledger.is_certified,
            "initial_score": initial_score,
            "final_score": ledger.score,
            "verdict": ledger.verdict,
            "fatal_defects_count": ledger.fatal_defects_count,
            "defects": ledger.defects,
            "elevated_brand": current_data,
            "executive_briefing": briefing,
            "summary": ledger.critic_verdict_summary
        }

    def _record_journal_entry(
        self,
        initial_score: int,
        final_score: int,
        is_certified: bool,
        fatal_defects: int,
        verdict: str
    ) -> None:
        try:
            self.journal.record_decision(
                iteration=1,
                target_file=self.target_path if self.target_path else "brand_tokens.css",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["aria_brand_visual_system_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, brand_data: Any, ledger: BrandDefectLedger) -> str:
        report = self.inspector.inspect(brand_data)
        m = report.metrics

        status_icon = "🎨 [LUMINARY CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED VISUAL DISSONANCE]"

        briefing = [
            f"# {status_icon} EXECUTIVE BRAND IDENTITY BRIEFING",
            f"**Auditor:** Aria 'The Luminary' Solano (Global Brand Director & Visual Identity Master)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## ✨ I. Visual System & Brand Harmony Matrix",
            f"- **Color Harmony & 60-30-10:** {'BALANCED (Semantic HSL Tokens)' if m.has_60_30_10_balance and not m.has_raw_primary_colors else 'UNBALANCED / RAW PRIMARIES DETECTED'}",
            f"- **Typographic Discipline:** {f'COHESIVE ({m.font_families_count} families, Modular Scale)' if m.font_families_count <= 2 and m.has_modular_type_scale else f'TYPOGRAPHIC ANARCHY ({m.font_families_count} families)'}",
            f"- **Vector Asset Precision:** {'VIEWBOX NORMALIZED (Responsive)' if m.has_svg_viewbox else 'MALFORMED (Missing viewBox)'}",
            f"- **Logo Clear-Space:** {'ENFORCED (1x Mark Safe Zone)' if m.has_logo_clear_space else 'UNPROTECTED (Crowding Hazard)'}",
            f"- **Brand Archetype & Voice:** {m.brand_archetype.upper()}",
            "",
            "## 🛑 II. Defect & Remediation Ledger",
        ]

        if not ledger.defects:
            briefing.append("✅ Zero brand defects identified. Visual system satisfies global luxury and Tier-1 product standards.")
        else:
            for d in ledger.defects:
                briefing.append(f"- **[{d.severity}] {d.title}:** {d.description}")
                briefing.append(f"  *Visual Impact:* {d.visual_impact}")
                briefing.append(f"  *Actionable Fix:* {d.actionable_fix}")

        briefing.extend([
            "",
            "## 🎨 III. Aria Solano's Visual Directive",
            ledger.critic_verdict_summary,
            ""
        ])

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Aria Solano: Global Brand Director Standalone Auditor"
    )
    parser.add_argument("target", nargs="?", default=None, help="Path to brand style guide or CSS token file")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed brand systems")
    parser.add_argument("--threshold", type=int, default=85, help="Minimum passing score")

    args = parser.parse_args()

    master = AriaSolanoMaster(target_path=args.target, passing_threshold=args.threshold)
    result = master.run_autonomous_cycle()

    print(result["executive_briefing"])

    if not result["is_certified"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
