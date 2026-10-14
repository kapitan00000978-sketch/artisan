"""Unit tests for Commander Orion 'The Deep' Sterling — Subsea Autonomous Robotics & Navigation Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #30.
"""

import pytest
from professions.deep_sea_subsea_architect.references import (
    DeepSeaReferenceLibrary,
    HydrostaticHullSpec,
    AcousticNavState,
    BuoyancySystemState,
    PressureCompensationState,
    calculate_hydrostatic_pressure,
    calculate_sound_speed_mackenzie,
    evaluate_hull_safety_factor,
    evaluate_net_buoyancy,
    STANDARD_GRAVITY,
    AVERAGE_HADAL_DENSITY,
)
from professions.deep_sea_subsea_architect.inspector import DeepSeaInspector
from professions.deep_sea_subsea_architect.rubric import DeepSeaRubric
from professions.deep_sea_subsea_architect.blind_critic import DeepSeaBlindCritic
from professions.deep_sea_subsea_architect.elevation_engine import DeepSeaElevationEngine
from professions.deep_sea_subsea_architect.master import OrionSterlingMaster, DeepSeaMaster


def test_hydrostatic_pressure_and_hull_spec():
    """Validates full ocean depth hydrostatic pressure calculations and hull safety factor."""
    # Depth = 11,000m, Hadal density = 1030 kg/m^3
    p_hadal = calculate_hydrostatic_pressure(11000.0, density_kg_m3=1030.0)
    assert p_hadal > 110.0  # Must exceed 110 MPa

    # Safety factor with 175 MPa collapse rating
    sf = evaluate_hull_safety_factor(175.0, p_hadal)
    assert sf >= 1.50

    # Certified titanium sphere specification
    safe_hull = HydrostaticHullSpec(
        material="Titanium Grade 5 (Ti-6Al-4V)",
        depth_rating_m=11000.0,
        collapse_pressure_mpa=175.0,
        operating_pressure_mpa=111.0,
        safety_factor=1.57,
        inner_diameter_m=1.2,
        wall_thickness_mm=65.0,
        yield_strength_mpa=880.0
    )
    assert safe_hull.is_hadal_certified() is True

    # Flawed shallow hull
    flawed_hull = HydrostaticHullSpec(
        material="Aluminum 6061-T6",
        depth_rating_m=4000.0,
        collapse_pressure_mpa=50.0,
        operating_pressure_mpa=45.0,
        safety_factor=1.11,
        inner_diameter_m=1.0,
        wall_thickness_mm=25.0,
        yield_strength_mpa=276.0
    )
    assert flawed_hull.is_hadal_certified() is False


def test_sound_speed_mackenzie_formula():
    """Validates empirical Mackenzie sound velocity profile calculation and acoustic navigation."""
    # Deep abyssal water: T = 2.0 C, S = 34.7 ppt, Depth = 5000m
    c = calculate_sound_speed_mackenzie(temperature_c=2.0, salinity_ppt=34.7, depth_m=5000.0)
    assert 1450.0 <= c <= 1550.0

    # Reliable acoustic state
    safe_nav = AcousticNavState(
        sound_speed_mps=c,
        dvl_bottom_lock=True,
        usbl_fix_valid=True,
        position_uncertainty_m=1.2,
        max_drift_threshold_m=2.0,
        acoustic_multipath_detected=False
    )
    assert safe_nav.is_navigation_reliable() is True

    # Unreliable state: lost bottom lock and high drift
    degraded_nav = AcousticNavState(
        sound_speed_mps=c,
        dvl_bottom_lock=False,
        usbl_fix_valid=False,
        position_uncertainty_m=6.5,
        max_drift_threshold_m=2.0,
        acoustic_multipath_detected=True
    )
    assert degraded_nav.is_navigation_reliable() is False


def test_dielectric_pressure_compensation_and_insulation():
    """Validates fluid pressure compensation bias and electrical isolation resistance."""
    # Intact system: 0.25 bar positive bias, 50 MOhm isolation
    healthy_comp = PressureCompensationState(
        reservoir_bias_pressure_bar=0.25,
        dielectric_fluid_type="Silicone Fluid 50 cSt",
        insulation_resistance_mohm=50.0,
        seawater_leak_detected=False,
        ambient_pressure_bar=1100.0
    )
    assert healthy_comp.is_compensation_intact() is True

    # Compromised system: negative bias and low insulation resistance
    compromised_comp = PressureCompensationState(
        reservoir_bias_pressure_bar=0.05,
        dielectric_fluid_type="Mineral Oil",
        insulation_resistance_mohm=0.5,
        seawater_leak_detected=True,
        ambient_pressure_bar=1100.0
    )
    assert compromised_comp.is_compensation_intact() is False


def test_variable_buoyancy_and_emergency_drop_weight():
    """Validates neutral buoyancy equilibrium and passive emergency ballast jettison."""
    # 1.0 m^3 displacement with 1030 kg mass in 1030 kg/m^3 water => 0 N net buoyancy
    net_b = evaluate_net_buoyancy(1.0, 1030.0, water_density_kg_m3=1030.0)
    assert pytest.approx(net_b, abs=1e-2) == 0.0

    # Healthy buoyancy system with 20s drop weight
    safe_buoyancy = BuoyancySystemState(
        displacement_volume_m3=1.5,
        vehicle_dry_mass_kg=1545.0,
        net_buoyancy_n=1.5,
        passive_drop_weight_kg=35.0,
        emergency_jettison_time_s=20.0,
        fail_safe_burn_wire_armed=True
    )
    assert safe_buoyancy.is_buoyancy_safe() is True

    # Dangerous buoyancy system: excessive drop time and unarmed burn wire
    unsafe_buoyancy = BuoyancySystemState(
        displacement_volume_m3=1.5,
        vehicle_dry_mass_kg=1600.0,
        net_buoyancy_n=-550.0,
        passive_drop_weight_kg=10.0,
        emergency_jettison_time_s=60.0,
        fail_safe_burn_wire_armed=False
    )
    assert unsafe_buoyancy.is_buoyancy_safe() is False


def test_deepsea_inspector_and_rubric():
    """Validates static AST inspection and 100-point rubric on canonical hadal code."""
    canonical_code = DeepSeaReferenceLibrary.get_canonical_core()
    metrics = DeepSeaInspector.inspect(canonical_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_hydrostatic_calc"] is True
    assert metrics["has_sound_speed_model"] is True
    assert metrics["has_hull_safety_check"] is True
    assert metrics["has_telemetry_eval"] is True
    assert metrics["has_passive_jettison"] is True
    assert metrics["has_fatal_defects"] is False

    score, breakdown, passed, veto_reason = DeepSeaRubric.evaluate(metrics)
    assert score >= 85.0
    assert passed is True
    assert veto_reason == ""
    assert breakdown["structural_crush"] > 0
    assert breakdown["code_determinism"] == 15.0


def test_blind_critic_catches_flaws():
    """Validates adversarial blind critic identifying substandard safety factor and missing fail-safes."""
    flawed_code = '''
def subsea_pilot(depth):
    # Shallow vehicle simulation
    max_depth_m = 3000.0
    min_safety_factor = 1.15
    compensation_bias_bar = 0.05
    emergency_jettison_time_s = 60.0
    max_drift_threshold_m = 8.0
    # TODO: add passive burn-wire drop weight
    raise NotImplementedError("burn wire not wired")
'''
    critique = DeepSeaBlindCritic.evaluate(flawed_code)
    assert critique["verdict"] == "REJECT"
    assert critique["passed"] is False
    assert critique["fatal_defects_count"] > 0
    assert any("Substandard hull collapse" in d["description"] for d in critique["defect_ledger"])


def test_elevation_engine_and_master_closed_loop():
    """Validates closed-loop elevation of flawed subsea code and master certification."""
    flawed_code = '''
def subsea_control(depth):
    max_depth_m = 4000.0
    min_safety_factor = 1.20
    # TODO: add hadal fail-safes
    return depth
'''
    elevation = DeepSeaElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85.0
    assert "HadalAutonomyExecutive" in elevation["elevated_code"] or "min_safety_factor = 1.50" in elevation["elevated_code"]

    master = OrionSterlingMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85.0
    assert result["verdict"] == "APPROVED"
    assert "COMMANDER ORION STERLING — EXECUTIVE SUBSEA HADAL BRIEFING" in result["executive_briefing"]
