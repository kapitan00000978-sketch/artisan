"""
Unit tests for Damian Vance (Principal Interactive Audio & Sound Subsystem).
"""

import pytest
from professions.audio_sound_architect.references import AudioReferenceLibrary, CANONICAL_WEB_AUDIO_CORE
from professions.audio_sound_architect.inspector import AudioSystemInspector
from professions.audio_sound_architect.rubric import AudioArchitectureRubric
from professions.audio_sound_architect.blind_critic import BlindAudioCritic
from professions.audio_sound_architect.elevation_engine import AudioElevationEngine
from professions.audio_sound_architect.master import DamianVanceMaster


def test_damian_references_loading():
    benchmarks = AudioReferenceLibrary.get_system_benchmarks()
    assert benchmarks["master_limiter_threshold_db"] == -0.5
    assert benchmarks["master_compressor_ratio"] == 12.0
    assert benchmarks["min_anti_click_ramp_seconds"] == 0.005

    adsr = AudioReferenceLibrary.get_adsr_profiles()
    assert "tactile_micro_click" in adsr
    assert "harmonic_notification_chime" in adsr
    assert adsr["tactile_micro_click"]["attack_s"] == 0.005

    anti_patterns = AudioReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "instant_gain_discontinuity_pop" for ap in anti_patterns)


def test_damian_inspector_clean_audio():
    inspector = AudioSystemInspector()
    report = inspector.inspect(CANONICAL_WEB_AUDIO_CORE)

    assert report.is_acoustic_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_audiocontext_unlock is True
    assert report.metrics.has_click_free_ramps is True
    assert report.metrics.has_instant_gain_jumps is False
    assert report.metrics.has_master_dynamics_compressor is True
    assert report.metrics.has_node_lifecycle_cleanup is True


def test_damian_inspector_flawed_audio():
    inspector = AudioSystemInspector()
    flawed_audio = (
        "class RawBeeper {\n"
        "    constructor() {\n"
        "        this.ctx = new AudioContext();\n"
        "    }\n"
        "    beep() {\n"
        "        const osc = this.ctx.createOscillator();\n"
        "        const gain = this.ctx.createGain();\n"
        "        gain.gain.value = 1.0;\n"
        "        osc.connect(gain);\n"
        "        gain.connect(this.ctx.destination);\n"
        "        osc.start();\n"
        "        gain.gain.value = 0;\n"
        "        osc.stop();\n"
        "    }\n"
        "}\n"
    )
    report = inspector.inspect(flawed_audio)

    assert report.is_acoustic_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_audiocontext_unlock is False
    assert report.metrics.has_instant_gain_jumps is True
    assert report.metrics.has_master_dynamics_compressor is False


def test_damian_rubric_and_veto():
    inspector = AudioSystemInspector()
    rubric = AudioArchitectureRubric()

    bad_audio = (
        "const ctx = new AudioContext();\n"
        "const gain = ctx.createGain();\n"
        "gain.gain.value = 0;\n"
        "gain.connect(ctx.destination);\n"
    )
    report = inspector.inspect(bad_audio)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 2


def test_damian_critic_defect_ledger():
    critic = BlindAudioCritic()
    flawed_audio = (
        "function playSound() {\n"
        "    const ctx = new AudioContext();\n"
        "    const osc = ctx.createOscillator();\n"
        "    osc.connect(ctx.destination);\n"
        "    osc.start();\n"
        "}\n"
    )
    ledger = critic.review(flawed_audio)

    assert ledger.verdict == "REJECTED_ACOUSTIC_DISSONANCE"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 2
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_damian_elevation_engine():
    engine = AudioElevationEngine()
    flawed_audio = (
        "class SimplePlayer {\n"
        "    init() {\n"
        "        this.ctx = new AudioContext();\n"
        "    }\n"
        "    play() {\n"
        "        const osc = this.ctx.createOscillator();\n"
        "        const gain = this.ctx.createGain();\n"
        "        osc.connect(gain);\n"
        "        gain.connect(this.ctx.destination);\n"
        "        osc.start();\n"
        "        gain.gain.value = 0;\n"
        "        osc.stop();\n"
        "    }\n"
        "}\n"
    )
    elevated_result = engine.elevate(flawed_audio)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "resume()" in elevated_result["elevated_audio"]
    assert "exponentialRampToValueAtTime" in elevated_result["elevated_audio"]
    assert "createDynamicsCompressor" in elevated_result["elevated_audio"]
    assert "onended" in elevated_result["elevated_audio"]


def test_damian_master_autonomous_cycle():
    master = DamianVanceMaster(passing_threshold=85)
    raw_audio = (
        "class RawBeeper {\n"
        "    constructor() { this.ctx = new AudioContext(); }\n"
        "    beep() {\n"
        "        const osc = this.ctx.createOscillator();\n"
        "        const gain = this.ctx.createGain();\n"
        "        gain.gain.value = 1;\n"
        "        osc.connect(gain);\n"
        "        gain.connect(this.ctx.destination);\n"
        "        osc.start();\n"
        "        gain.gain.value = 0;\n"
        "        osc.stop();\n"
        "    }\n"
        "}\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_audio)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE INTERACTIVE AUDIO BRIEFING" in result["executive_briefing"]
    assert "ACOUSTIC CERTIFIED" in result["executive_briefing"]
