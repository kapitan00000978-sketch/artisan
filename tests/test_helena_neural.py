#!/usr/bin/env python3
"""
Unit Test Suite for Dr. Helena 'The Synapse' Vance
Neural Interface & Biomechatronic BCI Architect Master Subsystem
"""

import math
import pytest
from professions.neural_interface_bci_architect import (
    shannon_safety_limit,
    tissue_temperature_rise,
    electrode_interface_impedance,
    biphasic_charge_balance_error,
    decoding_latency_budget,
    validate_neural_interface,
    NeuralInterfaceInspector,
    NeuralInterfaceRubric,
    NeuralInterfaceBlindCritic,
    NeuralInterfaceElevationEngine,
    DrHelenaVance
)


def test_shannon_safety_limit_calculation():
    # Microstimulation: Q = 0.05 uC/phase, geometric area A = 1.0e-3 cm^2 (1000 um^2)
    q = 0.05
    area = 1.0e-3
    k = shannon_safety_limit(q, area)
    # Expected: log10(50) + log10(0.05) ~ 1.69897 + (-1.30103) = 0.39794
    assert math.isclose(k, 0.39794, rel_tol=1e-4)
    assert k <= 1.75

    # Dangerous stimulation: Q = 2.0 uC/phase, area A = 1.0e-4 cm^2
    k_danger = shannon_safety_limit(2.0, 1.0e-4)
    # D = 20000, log10(20000) ~ 4.301, log10(2) ~ 0.301 => k ~ 4.602 > 1.75
    assert k_danger > 1.75

    with pytest.raises(ValueError):
        shannon_safety_limit(-1.0, area)


def test_tissue_temperature_rise():
    # Implant power 14 mW across 1.0 cm^2 cortical surface
    power_mw = 14.0
    area_cm2 = 1.0
    delta_t = tissue_temperature_rise(power_mw, area_cm2)
    # Expected: 14.0 / 40.0 = 0.35 deg C
    assert math.isclose(delta_t, 0.35, rel_tol=1e-5)
    assert delta_t <= 1.0

    with pytest.raises(ValueError):
        tissue_temperature_rise(-5.0, area_cm2)


def test_electrode_impedance_and_charge_balance():
    # Solution resistance Rs = 5000 Ohms, double-layer capacitance Cdl = 1.0 nF at 1000 Hz
    rs = 5000.0
    cdl = 1.0e-9
    freq = 1000.0
    z_mag = electrode_interface_impedance(rs, cdl, freq)
    # Xc = 1 / (2 * pi * 1000 * 1e-9) ~ 1.5915e5 Ohms (159.15 kohm)
    # |Z| = sqrt(5000^2 + 159155^2) approx 159.2 kohm
    z_kohm = z_mag / 1000.0
    assert 150.0 < z_kohm < 165.0

    # Biphasic charge balance: 10.0 pC cathodic vs 9.85 pC anodic
    residual_pc = biphasic_charge_balance_error(10.0, 9.85)
    assert math.isclose(residual_pc, 0.15, rel_tol=1e-5)

    # Decoding latency budget: 1.2ms spike detect + 1.0ms feature + 1.5ms inference + 0.5ms comm
    tau = decoding_latency_budget(1.2, 1.0, 1.5, 0.5)
    assert math.isclose(tau, 4.2, rel_tol=1e-5)


def test_validate_neural_interface():
    # Valid setup
    valid_res = validate_neural_interface(
        shannon_k=1.45,
        tissue_temp_rise_c=0.35,
        decoding_latency_ms=4.2,
        electrode_impedance_kohm=180.0,
        front_end_cmrr_db=105.0,
        residual_charge_pc=0.15
    )
    assert valid_res.is_valid is True
    assert len(valid_res.violations) == 0

    # Invalid setup
    invalid_res = validate_neural_interface(
        shannon_k=2.20,              # > 1.75
        tissue_temp_rise_c=1.85,     # > 1.0
        decoding_latency_ms=18.5,    # > 10.0
        electrode_impedance_kohm=750.0, # > 500.0
        front_end_cmrr_db=72.0,      # < 90.0
        residual_charge_pc=3.5       # > 1.0
    )
    assert invalid_res.is_valid is False
    assert len(invalid_res.violations) == 6


def test_neural_interface_inspector_and_rubric():
    inspector = NeuralInterfaceInspector()

    clean_code = """
def run_neural_bci_controller():
    shannon_safety = 1.45
    tissue_heating = 0.35
    decoding_latency = 4.2
    electrode_impedance = 180.0
    front_end_cmrr = 105.0
    residual_charge = 0.15
    return "Neuroprosthetic Locked and Active"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = NeuralInterfaceRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def run_neural_bci_controller():
    shannon_safety = 2.40
    tissue_heating = 2.10
    decoding_latency = 25.0
    electrode_impedance = 850.0
    front_end_cmrr = 65.0
    residual_charge = 4.8
    try:
        read_neural_dac_voltage()
    except Exception:
        pass
    return "Electrode Polarization Fault"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = NeuralInterfaceRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 6
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_blind_critic_adversarial_rejection():
    critic = NeuralInterfaceBlindCritic()
    toxic_stim = """
def stimulator_loop():
    shannon_safety = 2.65
    tissue_heating = 1.95
    residual_charge = 6.0
    return "Over-Stimulation"
"""
    audit = critic.audit(toxic_stim)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def bci_neuroprosthetic_executive():
    shannon_safety = 2.15
    tissue_heating = 1.60
    decoding_latency = 16.0
    electrode_impedance = 680.0
    front_end_cmrr = 75.0
    residual_charge = 3.2
    try:
        decode_motor_intention_stream()
    except Exception:
        pass
    return "Ataxic Drift"
"""
    master = DrHelenaVance(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="neural_bci_core.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Helena" in result["master"]
    assert len(result["actions_applied"]) >= 6

    # Verify that elevated code passes inspector with 100%
    inspector = NeuralInterfaceInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
