"""
Damian Vance - 100-Point Interactive Audio & Sound Architecture Rubric.

Evaluates Web Audio graphs, autoplay compliance, anti-click envelope shaping, and master dynamics limiting.
Passing threshold: 85/100 points.
Veto criteria: Unhandled browser autoplay lock, instant gain jump pops, or missing master compressor (clipping).
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from professions.audio_sound_architect.inspector import AudioInspectionReport, AudioMetrics


@dataclass
class AudioRubricEvaluation:
    total_score: int
    passing_threshold: int = 85
    is_certified: bool = False
    pillar_scores: Dict[str, int] = field(default_factory=dict)
    veto_triggered: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    remediation_recommendations: List[str] = field(default_factory=list)


class AudioArchitectureRubric:
    """Rigorous 100-point weighted evaluation rubric for interactive Web Audio and sound systems."""

    PASSING_THRESHOLD = 85

    def evaluate(self, report: AudioInspectionReport) -> AudioRubricEvaluation:
        m = report.metrics
        pillar_scores: Dict[str, int] = {}
        veto_reasons: List[str] = []
        recommendations: List[str] = []

        # ----------------------------------------------------
        # Pillar 1: Autoplay Policy & AudioContext Lifecycle (25 pts)
        # ----------------------------------------------------
        p1_score = 0
        if not m.has_audiocontext_unlock:
            veto_reasons.append(
                "Unhandled Browser Autoplay Policy: AudioContext created without checking context.state === 'suspended' or resume() on user gesture."
            )
            recommendations.append(
                "Wrap audio start in an async user gesture handler and call 'if (ctx.state === \"suspended\") await ctx.resume();'."
            )
        else:
            p1_score += 25

        pillar_scores["autoplay_lifecycle"] = p1_score

        # ----------------------------------------------------
        # Pillar 2: Click-Free Ramps & Zero-Transient Discipline (25 pts)
        # ----------------------------------------------------
        p2_score = 0
        if m.has_instant_gain_jumps:
            veto_reasons.append(
                "Instant Gain Discontinuity: Direct assignment of gain.value = 0 causes audible DC-offset speaker clicks/pops."
            )
            recommendations.append(
                "Replace instant assignments with gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + rampDuration)."
            )
        elif m.has_click_free_ramps:
            p2_score += 25
        else:
            p2_score += 5
            recommendations.append(
                "Use exponentialRampToValueAtTime or setTargetAtTime across all gain transitions to eliminate audio pops."
            )

        pillar_scores["click_free_ramps"] = p2_score

        # ----------------------------------------------------
        # Pillar 3: Master Dynamics Limiting & Anti-Clipping (20 pts)
        # ----------------------------------------------------
        p3_score = 0
        if not m.has_master_dynamics_compressor:
            veto_reasons.append(
                "Missing Master Dynamics Compressor: Audio nodes connect directly to destination without limiter headroom protection."
            )
            recommendations.append(
                "Route all active audio nodes through a master DynamicsCompressorNode (threshold: -0.5 dB, ratio: 12.0) before destination."
            )
        else:
            p3_score += 20

        pillar_scores["master_dynamics_compressor"] = p3_score

        # ----------------------------------------------------
        # Pillar 4: Hermetic Node Lifecycle Cleanup (15 pts)
        # ----------------------------------------------------
        p4_score = 0
        if m.has_node_lifecycle_cleanup:
            p4_score += 15
        else:
            p4_score += 4
            recommendations.append(
                "Register onended callbacks on oscillators and buffer sources: 'source.onended = () => { source.disconnect(); gain.disconnect(); };'."
            )

        pillar_scores["node_lifecycle_cleanup"] = p4_score

        # ----------------------------------------------------
        # Pillar 5: ADSR Psychoacoustic Shaping & Spatial Sound (15 pts)
        # ----------------------------------------------------
        p5_score = 0
        if m.has_adsr_envelope_shaping:
            p5_score += 10
        else:
            p5_score += 3
            recommendations.append(
                "Shape waveforms with attack, decay, sustain, and release phases to avoid sterile, piercing square tones."
            )

        if m.has_spatial_hrtf_panning:
            p5_score += 5
        else:
            p5_score += 2
            recommendations.append(
                "Incorporate HRTF spatial audio panners (createPanner) for immersive sound positioning."
            )

        pillar_scores["adsr_and_spatial_shaping"] = p5_score

        total_score = sum(pillar_scores.values())

        # Veto enforcement
        veto_triggered = len(veto_reasons) > 0
        if veto_triggered and total_score >= self.PASSING_THRESHOLD:
            total_score = 65

        is_certified = (total_score >= self.PASSING_THRESHOLD) and not veto_triggered

        return AudioRubricEvaluation(
            total_score=total_score,
            passing_threshold=self.PASSING_THRESHOLD,
            is_certified=is_certified,
            pillar_scores=pillar_scores,
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
            remediation_recommendations=recommendations
        )
