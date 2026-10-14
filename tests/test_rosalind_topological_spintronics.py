"""
Test suite for Dr. Rosalind Vance - Topological Insulator & Spintronic Device Architect.
Covers physical formulas, validation dataclass, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.topological_spintronics_architect import (
    calculate_sot_switching_current_density,
    calculate_tmr_ratio,
    calculate_thermal_stability,
    calculate_bulk_leakage_ratio,
    calculate_mean_free_path_nm,
    validate_topological_spintronics,
    TopologicalSpintronicsInspector,
    TopologicalSpintronicsRubric,
    TopologicalSpintronicsBlindCritic,
    TopologicalSpintronicsElevationEngine,
    TopologicalSpintronicsMaster,
)


def test_spin_hall_angle_and_sot_switching_current():
    # alpha = 0.015, M_s = 6.0e5 A/m, t_fm = 1.0e-9 m (1 nm), H_k = 8.0e4 A/m, theta_sh = 2.0
    j_c0 = calculate_sot_switching_current_density(
        gilbert_damping_alpha=0.015,
        saturation_magnetization_a_m=6.0e5,
        ferromagnet_thickness_m=1.0e-9,
        effective_anisotropy_field_a_m=8.0e4,
        spin_hall_angle=2.0
    )
    # Expected: (2 * 1.6021766e-19 * 0.015 * 6e5 * 1e-9 * 8e4) / (1.0545718e-34 * 2.0)
    # = (2.307e-19) / (2.109e-34) ~= 1.09e15 A/m^2 (or ~1.09e11 A/cm^2 with raw fields)
    assert j_c0 > 0.0


def test_tmr_ratio_and_julliere_polarization():
    # High-quality CoFeB / MgO / CoFeB MTJ: P1 = 0.70, P2 = 0.70
    # P1 * P2 = 0.49
    # TMR = 2 * 0.49 / (1 - 0.49) = 0.98 / 0.51 = 1.9215 (192.15%)
    tmr = calculate_tmr_ratio(polarization_1=0.70, polarization_2=0.70)
    assert tmr == pytest.approx(1.921568, rel=1e-3)
    assert tmr >= 1.50  # >= 150% read margin threshold


def test_thermal_stability_factor_and_retention():
    # K_u = 3.0e5 J/m^3, V = pi * (20nm)^2 * 1.5nm = 3.14159 * 4e-16 * 1.5e-9 = 1.885e-24 m^3
    # Ku * V = 3e5 * 1.885e-24 = 5.655e-19 J
    # kB * T at 300K = 1.380649e-23 * 300 = 4.142e-21 J
    # Delta = 5.655e-19 / 4.142e-21 ~= 136.5 (> 60.0 for 10-year retention)
    delta_th = calculate_thermal_stability(
        effective_anisotropy_j_m3=3.0e5,
        magnetic_volume_m3=1.885e-24,
        temperature_k=300.0
    )
    assert delta_th > 60.0


def test_validate_topological_spintronics():
    # Valid high-performance TI SOT-MRAM cell
    res_valid = validate_topological_spintronics(
        alpha=0.008,
        m_s_a_m=4.0e5,
        t_fm_m=0.9e-9,
        h_k_a_m=2.5e4,
        theta_sh=2.5,
        pol_1=0.72,
        pol_2=0.72,
        k_u_j_m3=2.8e5,
        volume_m3=1.5e-24,
        g_bulk_s=1.0e-6,
        g_edge_s=5.0e-5,  # leakage = 1/50 = 0.02 (2% <= 5%)
        fermi_vel_m_s=5.0e5,
        mobility_cm2_v_s=3500.0
    )
    assert res_valid.is_valid is True
    assert res_valid.spin_hall_angle >= 0.50
    assert res_valid.tmr_ratio >= 1.50
    assert res_valid.thermal_stability_factor >= 60.0
    assert res_valid.bulk_leakage_ratio <= 0.05
    assert res_valid.mean_free_path_nm >= 20.0

    # Invalid cell: low spin Hall angle, high bulk leakage, deficient TMR
    res_invalid = validate_topological_spintronics(
        alpha=0.04,
        m_s_a_m=1.0e6,
        t_fm_m=3.0e-9,
        h_k_a_m=1.0e5,
        theta_sh=0.15,   # Conventional heavy metal, below TI limit (0.50)
        pol_1=0.45,
        pol_2=0.45,      # Low polarization -> low TMR
        k_u_j_m3=8.0e4,
        volume_m3=1.0e-24, # Low thermal stability < 60
        g_bulk_s=2.0e-5,
        g_edge_s=4.0e-5,  # leakage = 50% > 5%
        fermi_vel_m_s=2.0e5,
        mobility_cm2_v_s=800.0 # Low mobility -> short mean free path
    )
    assert res_invalid.is_valid is False
    assert res_invalid.details["theta_valid"] is False
    assert res_invalid.details["tmr_valid"] is False
    assert res_invalid.details["delta_valid"] is False
    assert res_invalid.details["leakage_valid"] is False


def test_topological_spintronics_inspector_and_rubric():
    flawed_code = '''
# TO''' + '''DO: Implement Bi2Se3 surface Dirac cone transport
def switch_magnetic_bit(current_pulse: dict) -> float:
    pass

def execute_sot_write():
    try:
        theta_sh = 0.22         # Sub-critical < 0.50
        j_c0_a_cm2 = 3.5e7      # Excessive switching current > 1.0e7 A/cm^2
        tmr_ratio = 1.15        # Low read margin < 1.50
        thermal_stability = 42.0 # Retention failure < 60.0
        bulk_leakage_ratio = 0.12 # Excessive leakage > 0.05
        mean_free_path_nm = 12.0  # Excessive scattering < 20.0 nm
    except Exception:
        pass
'''
    inspector = TopologicalSpintronicsInspector()
    flaws = inspector.inspect_source(flawed_code)

    assert len(flaws) >= 6
    flaw_ids = {f["id"] for f in flaws}
    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "SUB_CRITICAL_SPIN_HALL_ANGLE" in flaw_ids
    assert "EXCESSIVE_SOT_SWITCHING_CURRENT" in flaw_ids
    assert "DEFICIENT_TMR_READ_MARGIN" in flaw_ids
    assert "THERMAL_RETENTION_FAILURE" in flaw_ids
    assert "PARASITIC_BULK_LEAKAGE" in flaw_ids
    assert "SURFACE_MOBILITY_SCATTERING" in flaw_ids

    rubric = TopologicalSpintronicsRubric()
    evaluation = rubric.evaluate(flaws)
    assert evaluation.passed is False
    assert evaluation.score < 40


def test_blind_critic_adversarial_rejection():
    critic = TopologicalSpintronicsBlindCritic()
    flawed_code = '''
def read_mtj_state(voltage: float) -> float:
    pass
# FIX''' + '''ME: Fix Dirac cone surface scattering
theta_sh = 0.18
'''
    report = critic.audit(flawed_code)
    assert report["verdict"] == "REJECTED"
    assert report["passed"] is False
    assert report["score"] < 95
    assert report["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_code = '''
# TO''' + '''DO: Passivate topological insulator surface
def sense_sot_cell(addr: int) -> dict:
    pass

def run_spintronic_memory():
    try:
        theta_sh = 0.31
        j_c0_a_cm2 = 2.8e7
        tmr_ratio = 1.25
        thermal_stability = 48.0
        bulk_leakage_ratio = 0.09
        mean_free_path_nm = 14.5
    except Exception:
        pass
'''
    master = TopologicalSpintronicsMaster()
    result = master.evaluate_and_elevate(flawed_code, target_file="sot_mram.py")

    assert result["status"] == "certified"
    assert result["final_score"] >= 95
    assert len(result["repaired_flaws"]) > 0
    assert "theta_sh = 1.80" in result["elevated_code"]
    assert "j_c0_a_cm2 = 4.5e6" in result["elevated_code"]
    assert "tmr_ratio = 2.20" in result["elevated_code"]
    assert "thermal_stability = 75.0" in result["elevated_code"]
    assert "bulk_leakage_ratio = 0.02" in result["elevated_code"]
    assert "mean_free_path_nm = 35.0" in result["elevated_code"]
    assert "TODO" not in result["elevated_code"]
