"""
Damian Vance - Interactive Sound & Audio Experience Reference Standards.

This module codifies empirical Web Audio benchmarks, psychoacoustic ADSR envelopes,
master dynamics limiting, and click-free waveform transition standards.
"""

from typing import Dict, Any, List


AUDIO_SYSTEM_BENCHMARKS: Dict[str, Any] = {
    "master_limiter_threshold_db": -0.5,
    "master_compressor_knee": 40.0,
    "master_compressor_ratio": 12.0,
    "master_compressor_attack": 0.003,
    "master_compressor_release": 0.250,
    "min_anti_click_ramp_seconds": 0.005,
    "target_integrated_loudness_lufs": -14.0,
    "standard_sample_rates": [44100, 48000]
}

ADSR_ENVELOPE_PROFILES: Dict[str, Dict[str, float]] = {
    "tactile_micro_click": {
        "attack_s": 0.005,
        "decay_s": 0.035,
        "sustain_level": 0.0,
        "release_s": 0.020,
        "base_freq_hz": 800.0
    },
    "harmonic_notification_chime": {
        "attack_s": 0.015,
        "decay_s": 0.080,
        "sustain_level": 0.35,
        "release_s": 0.180,
        "base_freq_hz": 523.25  # C5 harmonic
    },
    "spatial_ambient_pad": {
        "attack_s": 0.250,
        "decay_s": 0.400,
        "sustain_level": 0.70,
        "release_s": 0.800,
        "base_freq_hz": 220.0  # A3 warm root
    }
}

SPATIAL_ACOUSTIC_DEFAULTS: Dict[str, Any] = {
    "panning_model": "HRTF",
    "distance_model": "inverse",
    "ref_distance": 1.0,
    "max_distance": 10000.0,
    "rolloff_factor": 1.0,
    "cone_inner_angle": 360.0
}

TOXIC_AUDIO_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "unhandled_autoplay_suspension",
        "indicator": "Instantiating AudioContext or calling play() without handling context.state === 'suspended'.",
        "risk": "Fails silently in modern browsers due to autoplay policy; audio engine crashes on page load.",
        "severity": "FATAL"
    },
    {
        "id": "instant_gain_discontinuity_pop",
        "indicator": "Directly assigning gainNode.gain.value = 0 during playback without an exponential/linear ramp.",
        "risk": "Creates DC-offset waveform discontinuities, producing loud, harsh audible clicks and speaker pops.",
        "severity": "FATAL"
    },
    {
        "id": "missing_master_compressor_clipping",
        "indicator": "Connecting active sound generators directly to audioContext.destination without a DynamicsCompressorNode.",
        "risk": "Overlapping sound voices sum above 0dBFS, causing ear-piercing digital clipping distortion.",
        "severity": "FATAL"
    },
    {
        "id": "leaking_connected_audionodes",
        "indicator": "Creating oscillators, gain nodes, or audio buffer sources without disconnecting them upon completion.",
        "risk": "Garbage collector cannot reclaim audio thread memory; leads to CPU audio stutter and buffer underrun.",
        "severity": "HIGH"
    },
    {
        "id": "raw_unmodulated_waveform",
        "indicator": "Playing continuous unmodulated square/sawtooth waves at full amplitude without an ADSR envelope.",
        "risk": "Shrill, piercing, fatiguing acoustic profile that feels cheap and irritates users.",
        "severity": "HIGH"
    }
]

CANONICAL_WEB_AUDIO_CORE: str = (
    "// Damian Vance: Canonical Zero-Click Web Audio Architecture\n"
    "class ResonantAudioEngine {\n"
    "    constructor() {\n"
    "        this.ctx = null;\n"
    "        this.masterCompressor = null;\n"
    "    }\n"
    "    init() {\n"
    "        const AudioCtx = window.AudioContext || window.webkitAudioContext;\n"
    "        this.ctx = new AudioCtx();\n"
    "        this.masterCompressor = this.ctx.createDynamicsCompressor();\n"
    "        this.masterCompressor.threshold.setValueAtTime(-0.5, this.ctx.currentTime);\n"
    "        this.masterCompressor.ratio.setValueAtTime(12.0, this.ctx.currentTime);\n"
    "        this.masterCompressor.connect(this.ctx.destination);\n"
    "    }\n"
    "    async ensureActive() {\n"
    "        if (this.ctx && this.ctx.state === 'suspended') {\n"
    "            await this.ctx.resume();\n"
    "        }\n"
    "    }\n"
    "    playTactileClick() {\n"
    "        const now = this.ctx.currentTime;\n"
    "        const osc = this.ctx.createOscillator();\n"
    "        const gain = this.ctx.createGain();\n"
    "        osc.type = 'sine';\n"
    "        osc.frequency.setValueAtTime(800, now);\n"
    "        gain.gain.setValueAtTime(0.001, now);\n"
    "        gain.gain.exponentialRampToValueAtTime(0.3, now + 0.005);\n"
    "        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.040);\n"
    "        osc.connect(gain);\n"
    "        gain.connect(this.masterCompressor);\n"
    "        osc.start(now);\n"
    "        osc.stop(now + 0.045);\n"
    "        osc.onended = () => { osc.disconnect(); gain.disconnect(); };\n"
    "    }\n"
    "}\n"
)


class AudioReferenceLibrary:
    """Provides empirical audio benchmarks, ADSR envelope profiles, and Web Audio standards."""

    @staticmethod
    def get_system_benchmarks() -> Dict[str, Any]:
        return AUDIO_SYSTEM_BENCHMARKS

    @staticmethod
    def get_adsr_profiles() -> Dict[str, Dict[str, float]]:
        return ADSR_ENVELOPE_PROFILES

    @staticmethod
    def get_spatial_defaults() -> Dict[str, Any]:
        return SPATIAL_ACOUSTIC_DEFAULTS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_AUDIO_ANTI_PATTERNS

    @staticmethod
    def get_canonical_web_audio_core() -> str:
        return CANONICAL_WEB_AUDIO_CORE
