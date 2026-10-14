#!/usr/bin/env python3
"""
Unit Test Suite for Commander Zachary 'The Sub-Zero' Sterling
Cryogenic Superconducting & Dilution Refrigerator Systems Architect Master Subsystem
"""

import math
import pytest
from professions.cryogenic_superconducting_architect import (
    dilution_cooling_power_w,
    kapitza_temperature_drop,
    superconducting_critical_current,
    thermal_radiation_heat_leak_w,
    microphonic_detuning_hz,
    validate_cryogenic_fridge,
    CryogenicInspector,
    CryogenicRubric,
    CryogenicBlindCritic,
    CryogenicElevationEngine,
    CommanderZacharySterling
)


def test_dilution_cooling_power_calculation():
    # 3He circulation rate 100 umol/s = 1e-4 mol/s, T_mix = 10 mK = 0.01 K
    n_dot = 1.0e-4
    t_mix = 0.01
    q_dot_w = dilution_cooling_power_w(n_dot, t_mix)
    # Expected: 84 * 1e-4 * (0.01^2) = 84 * 1e-4 * 1e-4 = 84e-8 W = 0.84 uW
    assert math.isclose(q_dot_w, 8.4e-7, rel_tol=1e-5)
    q_dot_uw = q_dot_w * 1.0e6
    assert 0.8 < q_dot_uw < 0.9


def test_kapitza_thermal_boundary_resistance():
    # Heat flow 0.5 uW = 5e-7 W, boundary area 10 cm^2 = 1e-3 m^2, T = 15 mK = 0.015 K
    q_flow = 5.0e-7
    area = 1.0e-3
    t_boundary = 0.015
    delta_t = kapitza_temperature_drop(q_flow, area, t_boundary, kapitza_coeff=2.0e-3)
    # R_K = 2e-3 / (0.015^3) = 2e-3 / 3.375e-6 = 592.6 K*m^2/W
    # Delta_T = 592.6 * 5e-7 / 1e-3 = 0.296 K
    assert 0.1 < delta_t < 0.5


def test_superconducting_critical_current_surface():
    # NbTi wire: Ic0 = 100 A, Tc = 9.2 K, Bc2 = 14.5 T
    ic_0 = 100.0
    tc = 9.2
    bc2 = 14.5

    # At 4.2 K and 5.0 Tesla
    ic_op = superconducting_critical_current(ic_0, 4.2, tc, 5.0, bc2)
    assert 0 < ic_op < ic_0
    # Expected: 100 * (1 - (4.2/9.2)^2) * (1 - 5.0/14.5) ~ 100 * (1 - 0.208) * (1 - 0.345) ~ 51.8 A
    assert 48.0 < ic_op < 55.0

    # Above Tc: Ic must be 0
    ic_zero_t = superconducting_critical_current(ic_0, 10.0, tc, 5.0, bc2)
    assert ic_zero_t == 0.0

    # Above Bc2: Ic must be 0
    ic_zero_b = superconducting_critical_current(ic_0, 4.2, tc, 16.0, bc2)
    assert ic_zero_b == 0.0


def test_stefan_boltzmann_radiation_shielding():
    # Area 0.5 m^2 between 50K and 4K shields, MLI effective emissivity 0.03
    area = 0.5
    t_hot = 50.0
    t_cold = 4.2
    q_rad = thermal_radiation_heat_leak_w(area, t_hot, t_cold, emissivity_eff=0.03)
    # Expected: 5.67e-8 * 0.5 * 0.03 * (50^4 - 4.2^4) ~ 8.5e-10 * 6.25e6 ~ 0.0053 W (5.3 mW)
    assert 0.003 < q_rad < 0.008


def test_cryogenic_inspector_and_rubric():
    inspector = CryogenicInspector()

    clean_code = """
def run_dilution_fridge():
    base_temperature = 8.5
    superconducting_margin = 1.55
    parasitic_heat_leak = 0.35
    vibration_amplitude = 2.5e-5
    insulation_vacuum = 1.5e-8
    return "Stable at 8.5 mK"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = CryogenicRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def run_dilution_fridge():
    base_temperature = 28.0
    superconducting_margin = 1.05
    parasitic_heat_leak = 4.2
    vibration_amplitude = 8.0e-3
    insulation_vacuum = 5.0e-4
    try:
        sample_temperature()
    except Exception:
        pass
    return "Thermal Runaway"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = CryogenicRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 5
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_blind_critic_adversarial_rejection():
    critic = CryogenicBlindCritic()
    leaky_fridge = """
def cryostat_loop():
    base_temp_mk = 35.0
    sc_safety_factor = 1.10
    insulation_vacuum = 2.0e-3
    return "High Heat Leak"
"""
    audit = critic.audit(leaky_fridge)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def quantum_dilution_executive():
    base_temperature = 25.0
    superconducting_margin = 1.10
    parasitic_heat_leak = 3.5
    vibration_amplitude = 5.0e-4
    insulation_vacuum = 8.0e-5
    try:
        read_qubit_s_parameters()
    except Exception:
        pass
    return "Executed"
"""
    master = CommanderZacharySterling(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="cryostat_control.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Zachary" in result["master"]
    assert len(result["actions_applied"]) >= 5

    # Verify that elevated code passes inspector with 100%
    inspector = CryogenicInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
