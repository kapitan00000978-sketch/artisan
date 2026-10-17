"""
Test suite for Dr. Taras Sterling - Superfluid Quantum Hydrodynamics & Helium-4 Vortex Architect.
Covers physical formulas, validation dataclass, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.superfluid_hydrodynamics_architect import (
    CIRCULATION_QUANTUM,
    LANDAU_ROTON_VELOCITY_M_S,
    calculate_superfluid_fraction,
    calculate_feynman_critical_velocity,
    calculate_fountain_pressure,
    calculate_second_sound_velocity,
    calculate_vortex_mutual_friction,
    validate_superfluid_hydrodynamics,
    SuperfluidHydroInspector,
    SuperfluidHydroRubric,
    SuperfluidHydroBlindCritic,
    SuperfluidHydroElevationEngine,
    SuperfluidHydroMaster,
)


def test_two_fluid_fraction_and_circulation_quantum():
    # Quantum of circulation kappa = h / m_He4 ~= 9.9693e-8 m^2/s
    assert 9.9e-8 <= CIRCULATION_QUANTUM <= 1.01e-7

    # At 1.5 K: T/T_lambda = 1.5 / 2.1768 ~= 0.689
    # rho_s / rho = 1 - (0.689)^5.6 ~= 1 - 0.128 = 0.872 (87.2% superfluid)
    frac_1_5 = calculate_superfluid_fraction(1.5)
    assert 0.80 <= frac_1_5 <= 0.95

    # At T >= T_lambda (e.g. 2.2 K), superfluid fraction is zero
    assert calculate_superfluid_fraction(2.2) == 0.0


def test_feynman_and_landau_critical_velocities():
    # Capillary tube of diameter d = 100 micrometers (1.0e-4 m)
    v_c = calculate_feynman_critical_velocity(channel_diameter_m=1.0e-4)
    # v_c = (hbar / (m_He4 * d)) * ln(d / a_0)
    # prefactor = 1.054e-34 / (6.646e-27 * 1e-4) = 1.586e-4 m/s
    # log_factor = ln(1e-4 / 1e-10) = ln(1e6) ~= 13.815
    # v_c ~= 1.586e-4 * 13.815 ~= 2.19e-3 m/s = 2.19 mm/s
    assert 1.0e-3 <= v_c <= 5.0e-3
    assert v_c < LANDAU_ROTON_VELOCITY_M_S


def test_fountain_pressure_and_second_sound():
    # Fountain pressure: rho = 145.1 kg/m^3, S = 450 J/(kg K), Delta T = 0.05 K
    # Delta P = 145.1 * 450 * 0.05 = 3264.75 Pa
    p_fountain = calculate_fountain_pressure(density_kg_m3=145.1, entropy_j_kg_k=450.0, delta_t_k=0.05)
    assert p_fountain == pytest.approx(3264.75)

    # Second sound velocity: rho_s = 0.85, rho_n = 0.15, S = 450, T = 1.6 K, Cv = 750 J/(kg K)
    # c2 = sqrt((0.85 / 0.15) * (450^2 * 1.6 / 750)) = sqrt(5.6667 * 432) = sqrt(2448) ~= 49.4 m/s
    c2 = calculate_second_sound_velocity(
        rho_s_fraction=0.85,
        entropy_j_kg_k=450.0,
        temperature_k=1.6,
        specific_heat_j_kg_k=750.0
    )
    assert c2 > 12.0


def test_validate_superfluid_hydrodynamics():
    # Valid He-II quantum state
    res_valid = validate_superfluid_hydrodynamics(
        temperature_k=1.65,
        velocity_m_s=8.5,
        entropy_j_kg_k=480.0,
        specific_heat_j_kg_k=820.0,
        vortex_line_density_m2=2.5e9,
        superleak_pore_nm=4.0
    )
    assert res_valid.is_valid is True
    assert res_valid.superfluid_fraction >= 0.50
    assert res_valid.second_sound_velocity_m_s >= 12.0
    assert res_valid.vortex_line_density_m2 <= 1.0e12
    assert res_valid.superleak_pore_nm <= 10.0

    # Invalid state: T > T_lambda, high vortex density, large pore
    res_invalid = validate_superfluid_hydrodynamics(
        temperature_k=2.25,     # T > T_lambda
        velocity_m_s=65.0,      # > Landau limit
        entropy_j_kg_k=800.0,
        specific_heat_j_kg_k=1500.0,
        vortex_line_density_m2=5.0e12, # turbulent choking
        superleak_pore_nm=50.0   # pore allows normal fluid leaks
    )
    assert res_invalid.is_valid is False
    assert res_invalid.details["temp_valid"] is False
    assert res_invalid.details["velocity_valid"] is False
    assert res_invalid.details["vortex_valid"] is False
    assert res_invalid.details["pore_valid"] is False


def test_superfluid_hydro_inspector_and_rubric():
    flawed_code = '''
# TO''' + '''DO: Implement quantized vortex line reconnection
def circulate_superfluid(contour: list) -> float:
    pass

def execute_cryo_pumping():
    try:
        cryo_temperature = 2.45        # Above lambda transition > 2.10 K
        superfluid_fraction = 0.35     # Below 0.50 floor
        superfluid_velocity = 62.0     # Exceeds Landau roton limit
        vortex_line_density = 4.5e12   # Turbulent choking > 1.0e12 m^-2
        superleak_pore_nm = 35.0       # Viscous leakage > 10.0 nm
        second_sound_velocity = 8.5    # Second sound choking < 12.0 m/s
    except Exception:
        pass
'''
    inspector = SuperfluidHydroInspector()
    flaws = inspector.inspect_source(flawed_code)

    assert len(flaws) >= 6
    flaw_ids = {f["id"] for f in flaws}
    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "LAMBDA_TRANSITION_BREACH" in flaw_ids
    assert "SUPERFLUID_DENSITY_DEFICIT" in flaw_ids
    assert "LANDAU_ROTON_DISSIPATION" in flaw_ids
    assert "VORTEX_TANGLE_TURBULENCE" in flaw_ids
    assert "SUPERLEAK_VISCOUS_LEAKAGE" in flaw_ids
    assert "SECOND_SOUND_CHOKING" in flaw_ids

    rubric = SuperfluidHydroRubric()
    evaluation = rubric.evaluate(flaws)
    assert evaluation.passed is False
    assert evaluation.score < 40


def test_blind_critic_adversarial_rejection():
    critic = SuperfluidHydroBlindCritic()
    flawed_code = '''
def manage_fountain_pressure(delta_p: float) -> float:
    pass
# FIX''' + '''ME: Fix normal fluid viscous leak
cryo_temperature = 2.35
'''
    report = critic.audit(flawed_code)
    assert report["verdict"] == "REJECTED"
    assert report["passed"] is False
    assert report["score"] < 95
    assert report["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_code = '''
# TO''' + '''DO: Calibrate porous superleak sintered disk
def cool_superfluid_channel(stage: dict) -> dict:
    pass

def run_he_ii_loop():
    try:
        cryo_temperature = 2.30
        superfluid_fraction = 0.40
        superfluid_velocity = 58.5
        vortex_line_density = 3.2e12
        superleak_pore_nm = 25.0
        second_sound_velocity = 9.2
    except Exception:
        pass
'''
    master = SuperfluidHydroMaster()
    result = master.evaluate_and_elevate(flawed_code, target_file="superfluid_cryostat.py")

    assert result["status"] == "certified"
    assert result["final_score"] >= 95
    assert len(result["repaired_flaws"]) > 0
    assert "cryo_temperature = 1.65" in result["elevated_code"]
    assert "superfluid_fraction = 0.85" in result["elevated_code"]
    assert "superfluid_velocity = 12.0" in result["elevated_code"]
    assert "vortex_line_density = 4.5e9" in result["elevated_code"]
    assert "superleak_pore_nm = 4.0" in result["elevated_code"]
    assert "second_sound_velocity = 19.5" in result["elevated_code"]
    assert "TODO" not in result["elevated_code"]
