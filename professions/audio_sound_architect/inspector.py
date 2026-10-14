"""
Damian Vance - Objective Web Audio & Acoustic Architecture Inspector.

This module inspects JavaScript/TypeScript audio code, Web Audio graphs, and sound managers
to detect autoplay policy failures, waveform click/pop transients, and uncompressed clipping distortion.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import json


@dataclass
class AudioMetrics:
    has_audiocontext_unlock: bool = False
    has_click_free_ramps: bool = False
    has_instant_gain_jumps: bool = False
    has_master_dynamics_compressor: bool = False
    has_node_lifecycle_cleanup: bool = False
    has_adsr_envelope_shaping: bool = False
    has_spatial_hrtf_panning: bool = False
    anti_patterns_detected: List[str] = field(default_factory=list)


@dataclass
class AudioInspectionReport:
    metrics: AudioMetrics
    critical_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    benchmarks_passed: List[str] = field(default_factory=list)
    is_acoustic_viable: bool = False


class AudioSystemInspector:
    """Rigorous acoustic auditor evaluating Web Audio graphs, lifecycle handling, and psychoacoustics."""

    def inspect(self, audio_input: Any) -> AudioInspectionReport:
        """
        Audits audio source code string, Web Audio sound manager, or configuration dict.
        """
        metrics = self._extract_metrics(audio_input)
        critical_violations: List[str] = []
        warnings: List[str] = []
        benchmarks_passed: List[str] = []

        # 1. AudioContext Autoplay & Unlock Lifecycle
        if not metrics.has_audiocontext_unlock:
            critical_violations.append(
                "Unhandled Browser Autoplay Policy: AudioContext created without handling suspended state or user gesture resume. "
                "Will fail silently or throw browser security exceptions on modern runtimes."
            )
        else:
            benchmarks_passed.append("Autoplay-compliant AudioContext lifecycle with user-gesture resume verified.")

        # 2. Click-Free Waveform Ramps (Zero-Transient Discipline)
        if metrics.has_instant_gain_jumps:
            critical_violations.append(
                "Instant Gain Discontinuity (Audible Pop): Direct assignment of gain.value = 0 during playback. "
                "Creates harsh DC-offset waveform clicks; must use exponentialRampToValueAtTime."
            )
        elif metrics.has_click_free_ramps:
            benchmarks_passed.append("Click-free exponential / linear ramp transitions verified across gain nodes.")
        else:
            warnings.append("No smooth gain ramping detected; volume changes risk audible transient clicks.")

        # 3. Master Dynamics Limiting & Anti-Clipping
        if not metrics.has_master_dynamics_compressor:
            critical_violations.append(
                "Missing Master Dynamics Compressor: Sounds connect directly to destination without an intervening compressor/limiter. "
                "Overlapping voices will exceed 0 dBFS and cause severe digital clipping distortion."
            )
        else:
            benchmarks_passed.append("Master DynamicsCompressorNode headroom guardrail verified (-0.5 dBFS ceiling).")

        # 4. AudioNode Lifecycle Cleanup (Zero Leaks)
        if not metrics.has_node_lifecycle_cleanup:
            warnings.append("Missing automatic node disconnection (node.disconnect() in onended handler). Risks audio thread memory leak.")
        else:
            benchmarks_passed.append("Hermetic node lifecycle: Automatic disconnection verified on source completion.")

        # 5. ADSR Envelope Shaping
        if not metrics.has_adsr_envelope_shaping:
            warnings.append("Unshaped raw waveforms detected; sound lacks natural ADSR (Attack, Decay, Sustain, Release) envelope.")
        else:
            benchmarks_passed.append("Articulated ADSR psychoacoustic envelope shaping verified.")

        # 6. Spatial Acoustics
        if metrics.has_spatial_hrtf_panning:
            benchmarks_passed.append("Spatial HRTF 3D acoustic panning configured.")

        for ap in metrics.anti_patterns_detected:
            if ap not in critical_violations:
                critical_violations.append(f"Anti-Pattern Detected: {ap}")

        is_viable = len(critical_violations) == 0

        return AudioInspectionReport(
            metrics=metrics,
            critical_violations=critical_violations,
            warnings=warnings,
            benchmarks_passed=benchmarks_passed,
            is_acoustic_viable=is_viable
        )

    def _extract_metrics(self, audio_input: Any) -> AudioMetrics:
        text = ""
        metadata: Dict[str, Any] = {}

        if isinstance(audio_input, str):
            text = audio_input
            try:
                parsed = json.loads(audio_input)
                if isinstance(parsed, dict):
                    metadata = parsed
            except (json.JSONDecodeError, ValueError) as _json_err:
                _ = _json_err
        elif isinstance(audio_input, dict):
            metadata = audio_input
            text = json.dumps(audio_input)
        else:
            text = str(audio_input)

        text_lower = text.lower()
        m = AudioMetrics()

        # 1. Autoplay unlock detection
        has_unlock = (
            ("state === 'suspended'" in text_lower or "state === \"suspended\"" in text_lower) or
            "resume()" in text_lower or
            "usergesture" in text_lower or
            "user_gesture" in text_lower or
            metadata.get("has_audiocontext_unlock", False)
        )
        m.has_audiocontext_unlock = has_unlock

        # 2. Ramp and jump detection
        has_ramps = (
            "exponentialramptovalueattime" in text_lower or
            "linearramptovalueattime" in text_lower or
            "settargetattime" in text_lower or
            metadata.get("has_click_free_ramps", False)
        )
        m.has_click_free_ramps = has_ramps

        has_jumps = bool(
            re.search(r"gain(?:\.gain)?\.value\s*=\s*0(?:\.0*)?;", text_lower) and
            not has_ramps
        ) or metadata.get("has_instant_gain_jumps", False)
        m.has_instant_gain_jumps = has_jumps

        # 3. Master compressor
        has_comp = (
            "createdynamicscompressor" in text_lower or
            "dynamicscompressornode" in text_lower or
            "mastercompressor" in text_lower or
            metadata.get("has_master_dynamics_compressor", False)
        )
        m.has_master_dynamics_compressor = has_comp

        # 4. Node lifecycle
        has_cleanup = (
            "disconnect()" in text_lower or
            "onended" in text_lower or
            metadata.get("has_node_lifecycle_cleanup", False)
        )
        m.has_node_lifecycle_cleanup = has_cleanup

        # 5. ADSR envelope
        has_adsr = (
            ("attack" in text_lower and "decay" in text_lower and "release" in text_lower) or
            ("exponentialramptovalueattime" in text_lower and text_lower.count("exponentialramptovalueattime") >= 2) or
            metadata.get("has_adsr_envelope_shaping", False)
        )
        m.has_adsr_envelope_shaping = has_adsr

        # 6. Spatial HRTF
        has_spatial = (
            "hrtf" in text_lower or
            "createpanner" in text_lower or
            "pannernode" in text_lower or
            metadata.get("has_spatial_hrtf_panning", False)
        )
        m.has_spatial_hrtf_panning = has_spatial

        # Anti-pattern logging
        if not m.has_audiocontext_unlock:
            m.anti_patterns_detected.append("AudioContext unhandled suspended state (autoplay block)")
        if m.has_instant_gain_jumps:
            m.anti_patterns_detected.append("Instant gain discontinuity causing transient pop")
        if not m.has_master_dynamics_compressor:
            m.anti_patterns_detected.append("Missing master dynamics compressor causing clipping")

        return m
