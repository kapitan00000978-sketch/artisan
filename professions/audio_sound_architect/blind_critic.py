"""
Damian Vance - Blind Interactive Audio & Sound Critic.

Evaluates Web Audio graphs, interactive game soundscapes, and acoustic managers strictly
against zero-transient pop discipline, browser autoplay compliance, and dynamics limiting.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.audio_sound_architect.inspector import AudioSystemInspector, AudioInspectionReport
from professions.audio_sound_architect.rubric import AudioArchitectureRubric, AudioRubricEvaluation


@dataclass
class AudioDefect:
    defect_id: str
    severity: str  # FATAL, HIGH, MEDIUM
    title: str
    description: str
    acoustic_impact: str
    actionable_fix: str


@dataclass
class AudioDefectLedger:
    verdict: str  # CERTIFIED_IMMERSIVE_AUDIO or REJECTED_ACOUSTIC_DISSONANCE
    score: int
    passing_threshold: int
    is_certified: bool
    fatal_defects_count: int
    high_defects_count: int
    defects: List[AudioDefect] = field(default_factory=list)
    critic_verdict_summary: str = ""


class BlindAudioCritic:
    """Acoustic adversary reviewing interactive sound engines for clicks, distortion, and lifecycle leaks."""

    def __init__(self):
        self.inspector = AudioSystemInspector()
        self.rubric = AudioArchitectureRubric()

    def review(self, audio_input: Any) -> AudioDefectLedger:
        """
        Runs objective inspection and adversarial rubric scoring, producing an Audio Defect Ledger.
        """
        report: AudioInspectionReport = self.inspector.inspect(audio_input)
        eval_result: AudioRubricEvaluation = self.rubric.evaluate(report)

        defects: List[AudioDefect] = []

        # 1. Critical violations -> FATAL defects
        for i, violation in enumerate(report.critical_violations, start=1):
            if "autoplay" in violation.lower():
                title = "Unhandled Browser Autoplay Policy"
                impact = "Web Audio graph fails silently or throws security exception upon page load."
                fix = "Implement user gesture resume check: 'if (ctx.state === \"suspended\") await ctx.resume();'."
            elif "gain" in violation.lower() or "pop" in violation.lower() or "discontinuity" in violation.lower():
                title = "Instant Gain Discontinuity (Audible Transient Pop)"
                impact = "DC-offset discontinuity creates harsh, physical popping in headphones and speakers."
                fix = "Replace instantaneous assignments with exponentialRampToValueAtTime."
            elif "compressor" in violation.lower() or "clipping" in violation.lower():
                title = "Missing Master Dynamics Limiter (Digital Clipping)"
                impact = "Overlapping audio voices sum past 0 dBFS, inducing severe digital square-wave distortion."
                fix = "Insert a DynamicsCompressorNode between all gain nodes and context.destination."
            else:
                title = "Critical Audio Architecture Violation"
                impact = "Degrades acoustic fidelity or risks audio thread crash."
                fix = "Refactor Web Audio graph to Damian Vance zero-click acoustic standards."

            defects.append(
                AudioDefect(
                    defect_id=f"AUDIO-FATAL-{i:03d}",
                    severity="FATAL",
                    title=title,
                    description=violation,
                    acoustic_impact=impact,
                    actionable_fix=fix
                )
            )

        # 2. Veto reasons
        for j, reason in enumerate(eval_result.veto_reasons, start=len(defects) + 1):
            if not any(d.description == reason for d in defects):
                defects.append(
                    AudioDefect(
                        defect_id=f"AUDIO-FATAL-{j:03d}",
                        severity="FATAL",
                        title="Acoustic Integrity Veto",
                        description=reason,
                        acoustic_impact="Disqualifies the sound architecture from production deployment.",
                        actionable_fix="Address the corresponding veto requirement immediately."
                    )
                )

        # 3. Warnings -> HIGH / MEDIUM defects
        for k, warning in enumerate(report.warnings, start=len(defects) + 1):
            severity = "HIGH" if "disconnect" in warning.lower() or "envelope" in warning.lower() else "MEDIUM"
            if "disconnect" in warning.lower():
                title = "AudioNode Memory Leak (Missing Disconnection)"
                impact = "Dangling audio nodes prevent GC, causing audio thread stutter over extended sessions."
                fix = "Hook node.onended = () => { node.disconnect(); gain.disconnect(); }."
            elif "envelope" in warning.lower():
                title = "Unshaped Raw Waveform (Missing ADSR)"
                impact = "Sterile, harsh frequency output that fatigues the listener within seconds."
                fix = "Implement ADSR envelope curve on gain parameter."
            else:
                title = "Acoustic Suboptimality"
                impact = "Lacks dynamic spatial depth and acoustic polish."
                fix = "Follow Damian Vance recommendations."

            defects.append(
                AudioDefect(
                    defect_id=f"AUDIO-WARN-{k:03d}",
                    severity=severity,
                    title=title,
                    description=warning,
                    acoustic_impact=impact,
                    actionable_fix=fix
                )
            )

        fatal_count = sum(1 for d in defects if d.severity == "FATAL")
        high_count = sum(1 for d in defects if d.severity == "HIGH")

        verdict = (
            "CERTIFIED_IMMERSIVE_AUDIO"
            if eval_result.is_certified and fatal_count == 0
            else "REJECTED_ACOUSTIC_DISSONANCE"
        )

        summary = (
            f"Damian Vance Acoustic Review: Score {eval_result.total_score}/100. "
            f"Verdict: {verdict}. Fatal defects: {fatal_count}, High defects: {high_count}."
        )

        return AudioDefectLedger(
            verdict=verdict,
            score=eval_result.total_score,
            passing_threshold=eval_result.passing_threshold,
            is_certified=eval_result.is_certified and fatal_count == 0,
            fatal_defects_count=fatal_count,
            high_defects_count=high_count,
            defects=defects,
            critic_verdict_summary=summary
        )
