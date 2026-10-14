#!/usr/bin/env python3
"""
Unit Test Suite for Dr. Valentina 'The Sub-Atomic' Sterling
Scanning Probe Microscopy & Atomic Manipulation Architect Master Subsystem
"""

import math
import pytest
from professions.atomic_manipulation_architect import (
    tunneling_decay_constant,
    tunneling_current,
    qplus_frequency_shift,
    piezo_creep_displacement,
    validate_atomic_microscope,
    AtomicManipulationInspector,
    AtomicManipulationRubric,
    AtomicManipulationBlindCritic,
    AtomicManipulationElevationEngine,
    DrValentinaSterling
)


def test_tunneling_decay_and_current_calculation():
    # Work function 4.0 eV (e.g. Copper / Platinum tip-sample system)
    phi = 4.0
    kappa = tunneling_decay_constant(phi)
    # kappa ~ 1.025e10 m^-1 (approx 1.025 Angstrom^-1)
    assert 1.0e10 < kappa < 1.05e10

    # Tunneling current at 0.5 nm (5 Angstroms) gap, I0 = 10 nA
    i0 = 1.0e-8
    z_gap = 0.5e-9
    i_tunnel = tunneling_current(i0, z_gap, phi)
    assert 0 < i_tunnel < i0
    # Over 0.5 nm, 2 * kappa * z ~ 2 * 1.025e10 * 0.5e-9 = 10.25
    # exp(-10.25) ~ 3.5e-5 -> I ~ 3.5e-13 A (0.35 pA)
    assert 1.0e-14 < i_tunnel < 1.0e-11

    with pytest.raises(ValueError):
        tunneling_decay_constant(-1.0)
    with pytest.raises(ValueError):
        tunneling_current(-1.0, z_gap)


def test_qplus_frequency_shift_calculation():
    # f0 = 30 kHz = 30000 Hz, k = 1800 N/m, force gradient dF/dz = 0.5 N/m
    f0 = 30000.0
    k = 1800.0
    df_dz = 0.5
    delta_f = qplus_frequency_shift(f0, k, df_dz)
    # Expected: - (30000 / (2 * 1800)) * 0.5 = - (30000 / 3600) * 0.5 = -4.16667 Hz
    assert math.isclose(delta_f, -4.166666666666667, rel_tol=1e-5)

    with pytest.raises(ValueError):
        qplus_frequency_shift(-100.0, k, df_dz)


def test_piezo_creep_displacement():
    # Initial step x0 = 100 nm = 1e-7 m, at t = 100 s with t0 = 1 s, beta = 0.01
    x0 = 1.0e-7
    t = 100.0
    x_creep = piezo_creep_displacement(x0, t, t0_sec=1.0, beta=0.01)
    # Expected: 1e-7 * (1 + 0.01 * ln(100)) = 1e-7 * (1 + 0.01 * 4.60517) ~ 1e-7 * 1.04605 = 1.046e-7 m
    assert 1.04e-7 < x_creep < 1.05e-7

    # At or below t0: returns x0
    assert piezo_creep_displacement(x0, 0.5, t0_sec=1.0) == x0


def test_validate_atomic_microscope():
    # Valid setup
    valid_res = validate_atomic_microscope(
        thermal_drift_pm_h=1.8,
        vibration_amp_pm=0.35,
        base_pressure_mbar=2.5e-11,
        stage_temp_k=2.1,
        qplus_q_factor=32000.0,
        placement_accuracy_pm=8.5
    )
    assert valid_res.is_valid is True
    assert len(valid_res.violations) == 0

    # Invalid setup
    invalid_res = validate_atomic_microscope(
        thermal_drift_pm_h=12.0,       # > 5.0
        vibration_amp_pm=3.5,         # > 1.0
        base_pressure_mbar=5.0e-9,    # > 1.0e-10
        stage_temp_k=15.0,            # > 4.5
        qplus_q_factor=8000.0,        # < 25000.0
        placement_accuracy_pm=45.0    # > 20.0
    )
    assert invalid_res.is_valid is False
    assert len(invalid_res.violations) == 6


def test_atomic_manipulation_inspector_and_rubric():
    inspector = AtomicManipulationInspector()

    clean_code = """
def run_atomic_manipulator():
    thermal_drift = 1.8
    vibration_amp = 0.35
    base_pressure = 2.5e-11
    stage_temperature = 2.1
    qplus_q_factor = 32000.0
    placement_accuracy = 8.5
    return "Quantum Corral Fabricated"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = AtomicManipulationRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def run_atomic_manipulator():
    thermal_drift = 15.0
    vibration_amp = 4.2
    base_pressure = 8.0e-8
    stage_temperature = 22.0
    qplus_q_factor = 5000.0
    placement_accuracy = 65.0
    try:
        read_tunneling_photodiode()
    except Exception:
        pass
    return "Tip Crashed Into Substrate"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = AtomicManipulationRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 6
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_blind_critic_adversarial_rejection():
    critic = AtomicManipulationBlindCritic()
    leaky_spm = """
def spm_loop():
    thermal_drift = 18.0
    vibration_amp = 6.0
    base_pressure = 1.0e-7
    return "Drift Excessive"
"""
    audit = critic.audit(leaky_spm)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def single_atom_nanotech_executive():
    thermal_drift = 14.0
    vibration_amp = 2.8
    base_pressure = 4.0e-9
    stage_temperature = 12.0
    qplus_q_factor = 12000.0
    placement_accuracy = 35.0
    try:
        detect_tunneling_barrier()
    except Exception:
        pass
    return "Execution Drift"
"""
    master = DrValentinaSterling(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="atomic_manipulation_core.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Valentina" in result["master"]
    assert len(result["actions_applied"]) >= 6

    # Verify that elevated code passes inspector with 100%
    inspector = AtomicManipulationInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
