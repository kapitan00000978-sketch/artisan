"""
🌐 ZANE 'THE VECTOR' STERLING — TECHNICAL SEO & GROWTH ENGINEERING LEAD
Autonomous indexability conscience, Core Web Vitals inspection, blind crawl critique,
and automated Schema.org JSON-LD semantic elevation engine.

Usage:
    python professions/technical_seo_engineer/master.py <html_file> [--elevate]
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
    from .references import SEOReferenceLibrary
    from .inspector import SEOSystemInspector, SEOInspectionReport
    from .rubric import TechnicalSEORubric, SEORubricEvaluation
    from .blind_critic import BlindSEOCritic, SEODefectLedger
    from .elevation_engine import TechnicalSEOElevationEngine
except ImportError:
    from references import SEOReferenceLibrary
    from inspector import SEOSystemInspector, SEOInspectionReport
    from rubric import TechnicalSEORubric, SEORubricEvaluation
    from blind_critic import BlindSEOCritic, SEODefectLedger
    from elevation_engine import TechnicalSEOElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class ZaneSterlingMaster:
    """
    Zane Sterling: The living organic growth sovereign, Core Web Vitals guardian,
    and technical SEO conscience. Eliminates duplicate index penalties, enforces single H1
    hierarchies, and builds machine-readable Schema.org semantic graphs.
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
        self.inspector = SEOSystemInspector()
        self.rubric = TechnicalSEORubric()
        self.critic = BlindSEOCritic()
        self.elevation_engine = TechnicalSEOElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous technical SEO audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"SEO target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype flawed HTML page for testing or demo
            data = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head><title>Unoptimized Page</title></head>\n"
                "<body>\n"
                "    <h1>First Heading</h1>\n"
                "    <h1>Second Conflicting Heading</h1>\n"
                '    <img src="banner.jpg">\n'
                "</body>\n"
                "</html>\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: SEODefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_html"]
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
            "elevated_html": current_data,
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
                target_file=self.target_path if self.target_path else "index.html",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["zane_technical_seo_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, html_data: Any, ledger: SEODefectLedger) -> str:
        report = self.inspector.inspect(html_data)
        m = report.metrics

        status_icon = "🌐 [ORGANIC SOVEREIGN CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED INDEXABILITY FAILURE]"

        briefing = [
            f"# {status_icon} EXECUTIVE TECHNICAL SEO BRIEFING",
            f"**Auditor:** Zane 'The Vector' Sterling (Lead Technical SEO & Growth Engineering Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 1. Indexability Health & Core Web Vitals Metrics",
            f"- **H1 Heading Discipline:** {'PASS (Single H1)' if m.h1_count == 1 else f'FAIL ({m.h1_count} found)'}",
            f"- **Canonical URL Tag:** {'PASS (Declared)' if m.has_canonical_link else 'FAIL (Missing)'}",
            f"- **CLS Layout Stability:** {'PASS (Zero Unsized Images)' if m.images_missing_dimensions == 0 else f'FAIL ({m.images_missing_dimensions} unsized)'}",
            f"- **Schema.org Structured Data:** {'PASS (JSON-LD Active)' if m.has_schema_jsonld else 'WARN (Missing Rich Snippets)'}",
            f"- **Meta Description:** {'PASS (Present)' if m.has_meta_description else 'WARN (Missing)'}",
            f"- **Mobile Viewport:** {'PASS (Configured)' if m.has_viewport_meta else 'WARN (Missing)'}",
            f"- **Social Preview Cards:** {'PASS (OG + Twitter)' if m.has_opengraph_tags and m.has_twitter_card else 'WARN (Incomplete)'}",
            "",
            "## 2. Defects Ledger & Architectural Remediation",
        ]

        if ledger.defects:
            for d in ledger.defects:
                briefing.append(f"### [{d.severity}] {d.title} ({d.defect_id})")
                briefing.append(f"- **Description:** {d.description}")
                briefing.append(f"- **Ranking Impact:** {d.ranking_impact}")
                briefing.append(f"- **Actionable Fix:** {d.actionable_fix}")
                briefing.append("")
        else:
            briefing.append("Zero indexability or layout shift defects detected. Machine-readable organic dominance achieved.")

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Zane Sterling: Autonomous Technical SEO & Growth Engineering Master"
    )
    parser.add_argument("target", nargs="?", help="Path to HTML document or template file")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed HTML documents")
    parser.add_argument("--threshold", type=int, default=85, help="Passing score threshold (default: 85)")
    args = parser.parse_args()

    master = ZaneSterlingMaster(target_path=args.target, passing_threshold=args.threshold)
    results = master.run_autonomous_cycle()

    print(results["executive_briefing"])

    if args.elevate and "elevated_html" in results:
        print("\n--- ELEVATED TECHNICAL SEO HTML ---")
        print(results["elevated_html"])

    sys.exit(0 if results["is_certified"] else 1)


if __name__ == "__main__":
    main()
