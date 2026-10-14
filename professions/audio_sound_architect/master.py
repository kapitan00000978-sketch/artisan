"""
🔊 DAMIAN VANCE — PRINCIPAL INTERACTIVE AUDIO & SOUND ARCHITECT
Autonomous acoustic conscience, Web Audio graph inspection, blind transient critique,
and zero-click dynamics-compressed sound system elevation engine.

Usage:
    python professions/audio_sound_architect/master.py <audio_file> [--elevate]
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
    from .references import AudioReferenceLibrary
    from .inspector import AudioSystemInspector, AudioInspectionReport
    from .rubric import AudioArchitectureRubric, AudioRubricEvaluation
    from .blind_critic import BlindAudioCritic, AudioDefectLedger
    from .elevation_engine import AudioElevationEngine
except ImportError:
    from references import AudioReferenceLibrary
    from inspector import AudioSystemInspector, AudioInspectionReport
    from rubric import AudioArchitectureRubric, AudioRubricEvaluation
    from blind_critic import BlindAudioCritic, AudioDefectLedger
    from elevation_engine import AudioElevationEngine

# Import global ActiveDecisionJournal from studio engine
try:
    from src.studio.active_memory import ActiveDecisionJournal
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.studio.active_memory import ActiveDecisionJournal


class DamianVanceMaster:
    """
    Damian Vance: The living acoustic sovereign, Web Audio designer, and sound conscience.
    Eliminates waveform click/pop transients, enforces browser autoplay unlock compliance,
    and sculpts immersive, dynamically compressed soundscapes.
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
        self.inspector = AudioSystemInspector()
        self.rubric = AudioArchitectureRubric()
        self.critic = BlindAudioCritic()
        self.elevation_engine = AudioElevationEngine()
        self.journal = ActiveDecisionJournal()

    def run_autonomous_cycle(self, input_data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executes the closed-loop autonomous audio audit & elevation lifecycle.
        1. Inspect -> 2. Rubric -> 3. Critic -> 4. Elevate (if < 85) -> 5. Certify & Journal
        """
        data = input_data
        if data is None and self.target_path:
            if os.path.exists(self.target_path):
                with open(self.target_path, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                raise FileNotFoundError(f"Audio target file not found: {self.target_path}")

        if data is None:
            # Baseline prototype audio script for testing or demo
            data = (
                "// Flawed Web Audio Script\n"
                "class SoundController {\n"
                "    init() {\n"
                "        this.ctx = new AudioContext();\n"
                "    }\n"
                "    playBeep() {\n"
                "        const osc = this.ctx.createOscillator();\n"
                "        const gain = this.ctx.createGain();\n"
                "        gain.gain.value = 1.0;\n"
                "        osc.connect(gain);\n"
                "        gain.connect(this.ctx.destination);\n"
                "        osc.start();\n"
                "        setTimeout(() => { gain.gain.value = 0; osc.stop(); }, 100);\n"
                "    }\n"
                "}\n"
            )

        # Step 1: Initial Blind Critic Review
        ledger: AudioDefectLedger = self.critic.review(data)
        initial_score = ledger.score
        elevated_result: Optional[Dict[str, Any]] = None

        # Step 2: Elevate if failed
        current_data = data
        if not ledger.is_certified:
            elevated_result = self.elevation_engine.elevate(current_data, max_iterations=self.max_cycles)
            current_data = elevated_result["elevated_audio"]
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
            "elevated_audio": current_data,
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
                target_file=self.target_path if self.target_path else "audio_engine.js",
                defects_before=[f"Fatal defects: {fatal_defects}"],
                actions_taken=["damian_audio_zero_click_elevation"],
                score_before=float(initial_score),
                score_after=float(final_score)
            )
        except Exception as _journal_err:
            sys.stderr.write(f"Note: Decision journal record skipped: {_journal_err}\n")

    def _generate_briefing(self, audio_data: Any, ledger: AudioDefectLedger) -> str:
        report = self.inspector.inspect(audio_data)
        m = report.metrics

        status_icon = "🔊 [ACOUSTIC CERTIFIED]" if ledger.is_certified else "⚠️ [REJECTED ACOUSTIC DISSONANCE]"

        briefing = [
            f"# {status_icon} EXECUTIVE INTERACTIVE AUDIO BRIEFING",
            f"**Auditor:** Damian 'The Resonant' Vance (Principal Audio & Sound Architect)",
            f"**Final Score:** {ledger.score}/100 (Threshold: {ledger.passing_threshold})",
            f"**Verdict:** {ledger.verdict}",
            "",
            "## 1. Acoustic Health & System Metrics",
            f"- **Autoplay Unlock Handler:** {'PASS (Suspended State Checked)' if m.has_audiocontext_unlock else 'FAIL (Autoplay Blocked)'}",
            f"- **Click-Free Gain Ramping:** {'PASS (Exponential Envelope)' if m.has_click_free_ramps else 'FAIL (Transient Clicks Risk)'}",
            f"- **Instant Gain Discontinuities:** {'FAIL (Detected DC Pops)' if m.has_instant_gain_jumps else 'CLEAN (Zero Clicks)'}",
            f"- **Master Compressor Limiter:** {'PASS (DynamicsCompressorNode Active)' if m.has_master_dynamics_compressor else 'FAIL (Digital Clipping Risk)'}",
            f"- **Node Lifecycle Disconnection:** {'PASS (Hermetic Disconnect)' if m.has_node_lifecycle_cleanup else 'WARN (Potential Memory Leak)'}",
            f"- **ADSR Envelope Shaping:** {'PASS (Articulated ADSR)' if m.has_adsr_envelope_shaping else 'WARN (Raw Waveform)'}",
            f"- **Spatial HRTF Panning:** {'ACTIVE (3D Binaural)' if m.has_spatial_hrtf_panning else 'MONO / STEREO'}",
            "",
            "## 2. Defects Ledger & Acoustic Interventions",
        ]

        if ledger.defects:
            for d in ledger.defects:
                briefing.append(f"### [{d.severity}] {d.title} ({d.defect_id})")
                briefing.append(f"- **Description:** {d.description}")
                briefing.append(f"- **Acoustic Impact:** {d.acoustic_impact}")
                briefing.append(f"- **Actionable Fix:** {d.actionable_fix}")
                briefing.append("")
        else:
            briefing.append("Zero acoustic defects detected. Pristine psychoacoustic clarity and zero-transient discipline achieved.")

        return "\n".join(briefing)


def main():
    parser = argparse.ArgumentParser(
        description="Damian Vance: Autonomous Interactive Audio & Sound Architecture Master"
    )
    parser.add_argument("target", nargs="?", help="Path to Web Audio JavaScript or JSON config file")
    parser.add_argument("--elevate", action="store_true", help="Automatically elevate flawed audio scripts")
    parser.add_argument("--threshold", type=int, default=85, help="Passing score threshold (default: 85)")
    args = parser.parse_args()

    master = DamianVanceMaster(target_path=args.target, passing_threshold=args.threshold)
    results = master.run_autonomous_cycle()

    print(results["executive_briefing"])

    if args.elevate and "elevated_audio" in results:
        print("\n--- ELEVATED ACOUSTIC ARCHITECTURE ---")
        print(results["elevated_audio"])

    sys.exit(0 if results["is_certified"] else 1)


if __name__ == "__main__":
    main()
