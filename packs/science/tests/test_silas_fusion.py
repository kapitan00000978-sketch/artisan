"""Unit tests for Dr. Silas 'The Plasma' Vance — Tokamak Magnetic Confinement & Fusion Plasma Stability Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #29.
"""

import pytest
from professions.fusion_plasma_architect.references import (
    FusionReferenceLibrary,
    PlasmaEquilibrium,
    SafetyFactorProfile,
    TroyonBetaMonitor,
    GreenwaldDensityMonitor,
    NeoclassicalTearingMode,
    DivertorThermalProtection,
    MIN_SAFETY_FACTOR_Q95,
    KRUSKAL_SHAFRANOV_MIN_Q,
    MAX_TROYON_BETA_N,
    MAX_GREENWALD_FRACTION,
    MAX_DIVERTOR_HEAT_FLUX_MW_M2,
)
from professions.fusion_plasma_architect.inspector import FusionPlasmaInspector
from professions.fusion_plasma_architect.rubric import FusionPlasmaRubric
from professions.fusion_plasma_architect.blind_critic import FusionPlasmaBlindCritic
from professions.fusion_plasma_architect.elevation_engine import FusionPlasmaElevationEngine
from professions.fusion_plasma_architect.master import SilasVanceMaster


def test_plasma_equilibrium_and_safety_factor():
    """Validates tokamak plasma equilibrium parameters and Kruskal-Shafranov stability."""
    eq = PlasmaEquilibrium(
        major_radius_r0_m=6.2,
        minor_radius_a_m=2.0,
        b_toroidal_t=5.3,
        plasma_current_ma=15.0,
        electron_density_1e20=1.0,
        central_temperature_kev=20.0,
    )
    assert eq.aspect_ratio() == 6.2 / 2.0
    assert eq.cylindrical_safety_factor() > 0

    # Healthy profile: q0 = 1.05, q95 = 3.20 >= 3.0
    safe_profile = SafetyFactorProfile(q0=1.05, q95=3.20)
    stable, reasons = safe_profile.is_kruskal_shafranov_stable()
    assert stable is True
    assert len(reasons) == 0

    # Catastrophic external kink hazard: q95 < 2.0
    kink_profile = SafetyFactorProfile(q0=0.85, q95=1.80)
    stable, reasons = kink_profile.is_kruskal_shafranov_stable()
    assert stable is False
    assert any("external kink" in r for r in reasons)
    assert any("sawtooth" in r for r in reasons)


def test_troyon_beta_limit_calculations():
    """Validates normalized beta calculation and Troyon ideal MHD limit comparison."""
    # Healthy plasma: beta = 2.5%, a = 2.0m, B = 5.3T, Ip = 15 MA => beta_N = 2.5 * (2 * 5.3) / 15 = 1.767
    safe_beta = TroyonBetaMonitor(beta_total_pct=2.5, minor_radius_m=2.0, b_toroidal_t=5.3, plasma_current_ma=15.0)
    beta_n = safe_beta.normalized_beta()
    assert pytest.approx(beta_n, rel=1e-3) == 1.767
    assert safe_beta.is_within_troyon_limit(limit=3.5) is True

    # Ballooning instability runaway: beta = 6.0% => beta_N = 4.24 > 3.5
    unsafe_beta = TroyonBetaMonitor(beta_total_pct=6.0, minor_radius_m=2.0, b_toroidal_t=5.3, plasma_current_ma=15.0)
    assert unsafe_beta.normalized_beta() > 3.5
    assert unsafe_beta.is_within_troyon_limit(limit=3.5) is False


def test_greenwald_density_monitor():
    """Validates line-averaged electron density and Greenwald density fraction."""
    # a = 2.0m, Ip = 15 MA => Area = pi * 4 = 12.566 m^2 => n_G = 15 / 12.566 = 1.1937 * 10^20 m^-3
    # ne = 0.9 * 10^20 m^-3 => f_G = 0.9 / 1.1937 = 0.754 <= 0.85
    safe_density = GreenwaldDensityMonitor(electron_density_1e20=0.9, plasma_current_ma=15.0, minor_radius_m=2.0)
    assert safe_density.greenwald_fraction() < 0.85
    assert safe_density.is_safe_from_density_limit_disruption(max_fraction=0.85) is True

    # Radiative collapse / MARFE hazard: ne = 1.35 * 10^20 m^-3 => f_G = 1.35 / 1.1937 = 1.13 > 1.0
    unsafe_density = GreenwaldDensityMonitor(electron_density_1e20=1.35, plasma_current_ma=15.0, minor_radius_m=2.0)
    assert unsafe_density.greenwald_fraction() > 1.0
    assert unsafe_density.is_safe_from_density_limit_disruption(max_fraction=0.85) is False


def test_ntm_island_eccd_suppression():
    """Validates Neoclassical Tearing Mode island width and ECCD microwave stabilization."""
    # Small island (w = 0.08m, a = 2.0m => w/a = 0.04 <= 0.05)
    small_island = NeoclassicalTearingMode(rational_surface_q=1.5, island_width_m=0.08, minor_radius_m=2.0)
    assert small_island.is_stabilized(max_ratio=0.05) is True

    # Large island (w = 0.20m, a = 2.0m => w/a = 0.10) without ECCD
    unstable_island = NeoclassicalTearingMode(
        rational_surface_q=1.5, island_width_m=0.20, minor_radius_m=2.0, eccd_power_mw=0.0
    )
    assert unstable_island.is_stabilized(max_ratio=0.05) is False

    # Large island actively suppressed with 8 MW ECCD
    stabilized_island = NeoclassicalTearingMode(
        rational_surface_q=1.5, island_width_m=0.20, minor_radius_m=2.0, eccd_power_mw=8.0
    )
    assert stabilized_island.is_stabilized(max_ratio=0.05) is True


def test_divertor_thermal_protection():
    """Validates peak divertor heat exhaust against tungsten tile limit (<= 10 MW/m^2)."""
    safe_divertor = DivertorThermalProtection(peak_heat_flux_mw_m2=8.5, radiative_fraction=0.75)
    assert safe_divertor.is_divertor_protected(max_heat_flux=10.0, min_rad_fraction=0.70) is True

    unsafe_divertor = DivertorThermalProtection(peak_heat_flux_mw_m2=14.0, radiative_fraction=0.50)
    assert unsafe_divertor.is_divertor_protected(max_heat_flux=10.0, min_rad_fraction=0.70) is False


def test_inspector_and_rubric_evaluation():
    """Validates fusion inspector AST analysis, comment stripping, and 100-point rubric."""
    canonical_code = FusionReferenceLibrary.get_canonical_core()
    metrics = FusionPlasmaInspector.inspect(canonical_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_safety_factor_logic"] is True
    assert metrics["has_troyon_beta_logic"] is True
    assert metrics["has_greenwald_logic"] is True
    assert metrics["has_ntm_stabilization"] is True
    assert metrics["has_divertor_protection"] is True
    assert metrics["has_kink_disruption_hazard"] is False

    score, breakdown, passed, veto_reason = FusionPlasmaRubric.evaluate(metrics)
    assert score >= 85
    assert passed is True
    assert veto_reason == ""


def test_blind_critic_elevation_and_master():
    """Validates blind critique defect ledger, elevation engine remediation, and master runner."""
    flawed_code = '''
def run_plasma(ip):
    q95 = 1.8  # kink breach
    # TODO: add ECCD stabilization
    return ip
'''
    critique = FusionPlasmaBlindCritic.evaluate(flawed_code)
    assert critique["verdict"] == "REJECTED"
    assert critique["fatal_defects_count"] > 0

    elevation = FusionPlasmaElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85
    assert "SafetyFactorProfile" in elevation["elevated_code"]

    master = SilasVanceMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert result["verdict"] == "APPROVED"
    assert "EXECUTIVE FUSION PLASMA BRIEFING" in result["executive_briefing"]
