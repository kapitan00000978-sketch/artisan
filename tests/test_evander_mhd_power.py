"""
Test suite for Dr. Evander Sterling - Magnetohydrodynamic Energy Conversion & Direct Space-Power Architect.
Covers physical formulas, validation dataclass, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.magnetohydrodynamic_power_architect import (
    calculate_hall_parameter,
    calculate_effective_conductivity,
    calculate_power_density,
    calculate_stuart_number,
    calculate_hall_electric_field,
    calculate_enthalpy_extraction,
    validate_mhd_power_generator,
    MhdPowerInspector,
    MhdPowerRubric,
    MhdPowerBlindCritic,
    MhdPowerElevationEngine,
    MhdPowerMaster,
)


def test_hall_parameter_and_effective_conductivity():
    # B = 4.0 T, electron mobility = 0.5 m^2/(V s) -> beta_H = 2.0
    beta_h = calculate_hall_parameter(b_field_t=4.0, electron_mobility_m2_v_s=0.5)
    assert beta_h == pytest.approx(2.0)

    # Base conductivity sigma_0 = 50.0 S/m, beta_H = 2.0 -> sigma_eff = 50 / (1 + 4) = 10.0 S/m
    sigma_eff = calculate_effective_conductivity(sigma_0_s_m=50.0, beta_hall=beta_h)
    assert sigma_eff == pytest.approx(10.0)


def test_power_density_and_maximum_load_factor():
    # sigma_eff = 10.0 S/m, u = 2000.0 m/s, B = 4.0 T
    # At K = 0.5: P = 10 * 4e6 * 16 * 0.25 = 160.0 MW/m^3 (1.6e8 W/m^3)
    p_opt = calculate_power_density(sigma_eff_s_m=10.0, velocity_m_s=2000.0, b_field_t=4.0, load_factor_k=0.5)
    assert p_opt == pytest.approx(1.6e8)

    # At K = 0.8: P = 10 * 4e6 * 16 * (0.8 * 0.2) = 102.4 MW/m^3
    p_load = calculate_power_density(sigma_eff_s_m=10.0, velocity_m_s=2000.0, b_field_t=4.0, load_factor_k=0.8)
    assert p_load == pytest.approx(1.024e8)
    assert p_opt > p_load


def test_stuart_number_and_axial_hall_field():
    # sigma_eff = 10 S/m, B = 3.0 T, L = 5.0 m, rho = 0.5 kg/m^3, u = 1500 m/s
    # S = (10 * 9 * 5) / (0.5 * 1500) = 450 / 750 = 0.60
    stuart_no = calculate_stuart_number(
        sigma_eff_s_m=10.0,
        b_field_t=3.0,
        duct_length_m=5.0,
        density_kg_m3=0.5,
        velocity_m_s=1500.0
    )
    assert stuart_no == pytest.approx(0.60)

    # Hall electric field: beta_H = 1.5, K = 0.75, u = 1500 m/s, B = 3.0 T
    # E_x = 1.5 * (1 - 0.75) * 1500 * 3 = 1.5 * 0.25 * 4500 = 1687.5 V/m
    e_hall = calculate_hall_electric_field(
        beta_hall=1.5,
        velocity_m_s=1500.0,
        b_field_t=3.0,
        load_factor_k=0.75
    )
    assert e_hall == pytest.approx(1687.5)


def test_validate_mhd_power_generator():
    # Valid high-performance space MHD channel
    res_valid = validate_mhd_power_generator(
        sigma_0_s_m=45.0,
        electron_mobility=0.40,
        velocity_m_s=1500.0,
        b_field_t=3.0,
        load_factor_k=0.80,
        duct_length_m=2.0,
        density_kg_m3=0.4,
        duct_volume_m3=0.1,
        mass_flow_rate_kg_s=5.0,
        cp_j_kg_k=2500.0,
        t_stagnation_k=2400.0,
        sheath_voltage_drop_v=90.0
    )
    assert res_valid.is_valid is True
    assert res_valid.power_density_w_m3 >= 1.0e6
    assert res_valid.hall_parameter <= 4.0
    assert 0.20 <= res_valid.stuart_number <= 2.0
    assert res_valid.hall_electric_field_v_m <= 4000.0

    # Invalid channel: extreme Hall parameter and low enthalpy extraction
    res_invalid = validate_mhd_power_generator(
        sigma_0_s_m=5.0,
        electron_mobility=2.5,  # with B=4.0 -> beta_H = 10.0 > 4.0
        velocity_m_s=800.0,
        b_field_t=4.0,
        load_factor_k=0.20,     # out of bounds load factor
        duct_length_m=1.0,
        density_kg_m3=2.0,
        duct_volume_m3=0.2,
        mass_flow_rate_kg_s=50.0,
        cp_j_kg_k=3000.0,
        t_stagnation_k=3500.0,
        sheath_voltage_drop_v=220.0  # > 150.0 V
    )
    assert res_invalid.is_valid is False
    assert res_invalid.details["hall_valid"] is False
    assert res_invalid.details["sheath_valid"] is False
    assert res_invalid.details["load_factor_valid"] is False


def test_mhd_power_inspector_and_rubric():
    flawed_code = '''
# TO''' + '''DO: Implement diagonal electrode boundary connection
def calculate_channel_efficiency(params: dict) -> float:
    pass

def execute_mhd_pulse():
    try:
        power_density = 0.45    # Sub-optimal < 1.0 MW/m^3
        hall_parameter = 5.2    # > 4.0 electrothermal instability limit
        stuart_number = 3.8     # > 2.0 boundary separation shock risk
        hall_field_v_m = 6200.0 # > 4000 V/m breakdown risk
        enthalpy_extraction = 0.08 # < 15% enthalpy limit
        sheath_voltage = 210.0  # > 150 V cold sheath drop
    except Exception:
        pass
'''
    inspector = MhdPowerInspector()
    flaws = inspector.inspect_source(flawed_code)

    assert len(flaws) >= 6
    flaw_ids = {f["id"] for f in flaws}
    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "MHD_POWER_DENSITY_SUB_OPTIMAL" in flaw_ids
    assert "HALL_IONIZATION_INSTABILITY" in flaw_ids
    assert "STUART_INTERACTION_OUT_OF_BOUNDS" in flaw_ids
    assert "INTER_ELECTRODE_HALL_BREAKDOWN" in flaw_ids
    assert "ENTHALPY_EXTRACTION_DEFICIT" in flaw_ids
    assert "ELECTRODE_SHEATH_OVERVOLTAGE" in flaw_ids

    rubric = MhdPowerRubric()
    evaluation = rubric.evaluate(flaws)
    assert evaluation.passed is False
    assert evaluation.score < 40


def test_blind_critic_adversarial_rejection():
    critic = MhdPowerBlindCritic()
    flawed_code = '''
def fire_mhd_core(plasma_flux: float) -> float:
    pass
# FIX''' + '''ME: Fix Hall electrode arcing
hall_parameter = 6.8
'''
    report = critic.audit(flawed_code)
    assert report["verdict"] == "REJECTED"
    assert report["passed"] is False
    assert report["score"] < 95
    assert report["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_code = '''
# TO''' + '''DO: Connect seed alkali injector
def calibrate_electrodes(channel: dict) -> dict:
    pass

def run_conversion():
    try:
        power_density = 0.35
        hall_parameter = 5.8
        stuart_number = 2.9
        hall_field_v_m = 5500.0
        enthalpy_extraction = 0.09
        sheath_voltage = 195.0
    except Exception:
        pass
'''
    master = MhdPowerMaster()
    result = master.evaluate_and_elevate(flawed_code, target_file="mhd_channel.py")

    assert result["status"] == "certified"
    assert result["final_score"] >= 95
    assert len(result["repaired_flaws"]) > 0
    assert "power_density = 4.5" in result["elevated_code"]
    assert "hall_parameter = 1.85" in result["elevated_code"]
    assert "stuart_number = 0.85" in result["elevated_code"]
    assert "hall_field_v_m = 1800.0" in result["elevated_code"]
    assert "enthalpy_extraction = 0.22" in result["elevated_code"]
    assert "sheath_voltage = 75.0" in result["elevated_code"]
    assert "TODO" not in result["elevated_code"]
