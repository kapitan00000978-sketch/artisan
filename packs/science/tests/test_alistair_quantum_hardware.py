"""Unit tests for Dr. Alistair 'The Flux' Vance — Quantum Hardware & Microwave Pulse Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #27.
"""

import pytest
from professions.quantum_hardware_architect.references import (
    QuantumHardwareReferenceLibrary,
    QubitCoherenceProfile,
    DragPulse,
    ReadoutResonator,
    QuantumGatePulse,
    QuantumCircuitSchedule,
    MIN_SINGLE_QUBIT_FIDELITY,
    MIN_T1_RELAXATION_US,
    MIN_T2_DEPHASING_US,
)
from professions.quantum_hardware_architect.inspector import QuantumHardwareInspector
from professions.quantum_hardware_architect.rubric import QuantumHardwareRubric
from professions.quantum_hardware_architect.blind_critic import QuantumHardwareBlindCritic
from professions.quantum_hardware_architect.elevation_engine import QuantumHardwareElevationEngine
from professions.quantum_hardware_architect.master import AlistairVanceMaster


def test_qubit_coherence_profile_physics():
    """Validates transmon coherence rates and physical bounds (T2 <= 2*T1, negative anharmonicity)."""
    healthy_qubit = QubitCoherenceProfile(
        qubit_id=0,
        t1_us=80.0,
        t2_us=60.0,
        frequency_ghz=5.12,
        anharmonicity_mhz=-310.0,
    )
    assert healthy_qubit.relaxation_rate_khz() == 1000.0 / 80.0
    assert healthy_qubit.dephasing_rate_khz() == 1000.0 / 60.0
    sound, reasons = healthy_qubit.is_physically_sound()
    assert sound is True
    assert len(reasons) == 0

    # Test thermodynamic violation: T2 > 2*T1
    unphysical_qubit = QubitCoherenceProfile(
        qubit_id=1,
        t1_us=40.0,
        t2_us=100.0,  # Violates T2 <= 2*T1
        frequency_ghz=4.95,
        anharmonicity_mhz=20.0,  # Violates negative anharmonicity
    )
    sound, reasons = unphysical_qubit.is_physically_sound()
    assert sound is False
    assert any("Unphysical dephasing" in r for r in reasons)
    assert any("negative anharmonicity" in r for r in reasons)


def test_drag_pulse_waveform_generation():
    """Validates DRAG microwave pulse discretization on 2.4 Gsps AWG clock."""
    pulse = DragPulse(
        duration_ns=20.0,
        amplitude=0.8,
        sigma_ns=4.0,
        beta_drag=0.5,
        phase_rad=0.0,
    )
    # At 2.4 Gsps, 20 ns = 48 samples
    i_samples, q_samples = pulse.generate_waveform(sample_rate_gsps=2.4)
    assert len(i_samples) == 48
    assert len(q_samples) == 48

    # Peak of Gaussian should be near center
    mid = len(i_samples) // 2
    assert i_samples[mid] > 0.7
    # Derivative should cross zero near center
    assert abs(q_samples[mid] + q_samples[mid - 1]) < 0.2


def test_drag_pulse_parameter_validation():
    """Validates physical pulse limits and Gaussian truncation bounds (> 4*sigma)."""
    valid_pulse = DragPulse(duration_ns=24.0, amplitude=0.9, sigma_ns=5.0, beta_drag=0.3)
    sound, errors = valid_pulse.validate()
    assert sound is True
    assert len(errors) == 0

    invalid_pulse = DragPulse(duration_ns=10.0, amplitude=1.5, sigma_ns=4.0, beta_drag=0.3)
    # amplitude > 1.0 and 4*sigma (16ns) > duration (10ns)
    sound, errors = invalid_pulse.validate()
    assert sound is False
    assert any("Amplitude out of DAC range" in e for e in errors)
    assert any("Gaussian truncation error" in e for e in errors)


def test_readout_resonator_dispersive_shift():
    """Validates dispersive readout cavity shift and ground/excited state separation."""
    resonator = ReadoutResonator(
        qubit_id=0,
        bare_frequency_ghz=7.200,
        dispersive_shift_chi_mhz=-1.5,
        integration_window_ns=1200.0,
    )
    assert pytest.approx(resonator.ground_state_frequency_ghz(), rel=1e-5) == 7.1985
    assert pytest.approx(resonator.excited_state_frequency_ghz(), rel=1e-5) == 7.2015
    assert resonator.frequency_separation_mhz() == 3.0


def test_quantum_circuit_schedule_coherence_budget():
    """Validates pulse schedule duration against 5% coherence horizon budget."""
    q0 = QubitCoherenceProfile(qubit_id=0, t1_us=100.0, t2_us=80.0, frequency_ghz=5.0)
    pulse = DragPulse(duration_ns=20.0, amplitude=0.5, sigma_ns=4.0, beta_drag=0.1)

    gate = QuantumGatePulse(name="X90", target_qubits=[0], pulse=pulse, fidelity=0.9995)
    assert gate.is_certified() is True

    schedule = QuantumCircuitSchedule(qubits=[q0], gates=[gate] * 10)  # 200 ns total
    assert schedule.total_duration_ns() == 200.0

    valid_budget, reasons = schedule.validate_coherence_budget()
    assert valid_budget is True
    assert len(reasons) == 0


def test_inspector_and_rubric_evaluation():
    """Validates quantum inspector AST analysis, comment stripping, and rubric vetoes."""
    canonical_code = QuantumHardwareReferenceLibrary.get_canonical_core()
    metrics = QuantumHardwareInspector.inspect(canonical_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_drag_pulse"] is True
    assert metrics["has_coherence_guard"] is True
    assert metrics["has_anharmonicity_logic"] is True
    assert metrics["has_fidelity_verification"] is True
    assert metrics["has_readout_resonator"] is True
    assert metrics["has_square_pulse_hazard"] is False

    score, breakdown, passed, veto_reason = QuantumHardwareRubric.evaluate(metrics)
    assert score >= 85
    assert passed is True
    assert veto_reason == ""

    # Test veto on unshaped square pulse
    bad_code = "def drive_qubit(): square_pulse(duration=20) # raw square drive"
    bad_metrics = QuantumHardwareInspector.inspect(bad_code)
    bad_score, _, bad_passed, bad_veto = QuantumHardwareRubric.evaluate(bad_metrics)
    assert bad_passed is False
    assert "QuantumLeakageHazard" in bad_veto


def test_blind_critic_elevation_and_master():
    """Validates blind critic defect ledger, elevation engine remediation, and master runner."""
    flawed_code = '''
def apply_microwave_drive(qubit_id):
    square_pulse(duration=20)
    return True
'''
    critique = QuantumHardwareBlindCritic.evaluate(flawed_code)
    assert critique["verdict"] == "REJECTED"
    assert critique["fatal_defects_count"] > 0

    elevation = QuantumHardwareElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85
    assert "DragPulse" in elevation["elevated_code"]

    master = AlistairVanceMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert result["verdict"] == "APPROVED"
    assert "EXECUTIVE QUANTUM HARDWARE BRIEFING" in result["executive_briefing"]
