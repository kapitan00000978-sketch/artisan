"""Unit tests for Dr. Zephyr 'The Hypersonic' Sterling — Hypersonic Aerothermodynamics & Scramjet Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #31.
"""

import pytest
from professions.hypersonic_aerodynamics_architect.references import (
    HypersonicReferenceLibrary,
    HypersonicFreestreamState,
    ShockLayerThermodynamics,
    ScramjetIsolatorState,
    ThermalProtectionState,
    calculate_stagnation_temperature,
    calculate_sutton_graves_heat_flux,
    calculate_isolator_shock_train_length,
    evaluate_isolator_stability_margin,
    evaluate_tps_safety_factor,
    SUTTON_GRAVES_CONSTANT,
)
from professions.hypersonic_aerodynamics_architect.inspector import HypersonicInspector
from professions.hypersonic_aerodynamics_architect.rubric import HypersonicRubric
from professions.hypersonic_aerodynamics_architect.blind_critic import HypersonicBlindCritic
from professions.hypersonic_aerodynamics_architect.elevation_engine import HypersonicElevationEngine
from professions.hypersonic_aerodynamics_architect.master import ZephyrSterlingMaster, HypersonicMaster


def test_hypersonic_freestream_and_stagnation_temperature():
    """Validates hypersonic freestream regime boundaries and stagnation temperature calculation."""
    # Mach 7.0 at 30km altitude (T = 226.5 K)
    state = HypersonicFreestreamState(
        mach_number=7.0,
        altitude_m=30000.0,
        velocity_mps=2110.0,
        ambient_temperature_k=226.5,
        ambient_pressure_pa=1197.0,
        density_kg_m3=0.0184
    )
    assert state.is_hypersonic_regime() is True

    # Stagnation temperature: T0 = 226.5 * (1 + 0.2 * 49) = 226.5 * 10.8 = 2446.2 K
    t0 = calculate_stagnation_temperature(state.ambient_temperature_k, state.mach_number)
    assert pytest.approx(t0, rel=1e-2) == 2446.2

    # Non-hypersonic regime (Mach 3.5)
    supersonic_state = HypersonicFreestreamState(
        mach_number=3.5,
        altitude_m=15000.0,
        velocity_mps=1030.0,
        ambient_temperature_k=216.6,
        ambient_pressure_pa=12111.0,
        density_kg_m3=0.194
    )
    assert supersonic_state.is_hypersonic_regime() is False


def test_sutton_graves_aerothermal_heat_flux():
    """Validates Sutton-Graves stagnation heat flux calculation and TPS safety factors."""
    # Freestream density = 0.02 kg/m^3, velocity = 2500 m/s, nose radius = 0.05 m
    q_stag = calculate_sutton_graves_heat_flux(
        density_kg_m3=0.02,
        velocity_mps=2500.0,
        nose_radius_m=0.05
    )
    assert q_stag > 0.0  # MW/m^2

    # Healthy TPS state: material limit = 12.0 MW/m^2, actual = 6.5 MW/m^2, SF = 1.84 >= 1.50
    safe_tps = ThermalProtectionState(
        peak_heat_flux_mw_m2=6.5,
        nose_radius_m=0.05,
        surface_temperature_k=2150.0,
        material_limit_temperature_k=2500.0,
        tps_safety_factor=1.84
    )
    assert safe_tps.is_tps_safe() is True

    # Flawed TPS state: safety factor below 1.50 and overtemperature
    unsafe_tps = ThermalProtectionState(
        peak_heat_flux_mw_m2=14.0,
        nose_radius_m=0.02,
        surface_temperature_k=2800.0,
        material_limit_temperature_k=2500.0,
        tps_safety_factor=1.10
    )
    assert unsafe_tps.is_tps_safe() is False


def test_real_gas_shock_dissociation_and_limits():
    """Validates non-equilibrium real-gas dissociation threshold above 2000K."""
    # Post-shock temperature 3800K with active dissociation and reduced gamma
    real_gas = ShockLayerThermodynamics(
        stagnation_temperature_k=4200.0,
        post_shock_temperature_k=3800.0,
        dissociation_fraction_o2=0.45,
        dissociation_fraction_n2=0.08,
        is_real_gas_active=True,
        specific_heat_ratio_effective=1.28
    )
    assert real_gas.is_real_gas_valid() is True

    # Flawed: high temperature shock layer modeled as ideal gas without dissociation
    ideal_gas_hazard = ShockLayerThermodynamics(
        stagnation_temperature_k=4200.0,
        post_shock_temperature_k=3800.0,
        dissociation_fraction_o2=0.0,
        dissociation_fraction_n2=0.0,
        is_real_gas_active=False,
        specific_heat_ratio_effective=1.40
    )
    assert ideal_gas_hazard.is_real_gas_valid() is False


def test_scramjet_isolator_stability_and_unstart_margins():
    """Validates Waltrup-Billig shock train length and isolator stability margin."""
    # Isolator height = 0.1 m, combustor pressure ratio = 3.5 => L_st = 0.1 * 1.4 * 2.5 = 0.35 m
    l_st = calculate_isolator_shock_train_length(isolator_height_m=0.1, pressure_ratio_combustor_to_inlet=3.5)
    assert pytest.approx(l_st, rel=1e-3) == 0.35

    # Isolator length = 0.50 m => margin = 0.50 / 0.35 = 1.428 >= 1.25
    margin = evaluate_isolator_stability_margin(isolator_length_m=0.50, shock_train_length_m=l_st)
    assert margin >= 1.25

    # Safe isolator state
    safe_isolator = ScramjetIsolatorState(
        isolator_length_m=0.50,
        isolator_height_m=0.1,
        shock_train_length_m=0.35,
        combustor_to_inlet_pressure_ratio=3.5,
        isolator_stability_margin=margin,
        response_time_ms=2.5,
        is_unstart_imminent=False
    )
    assert safe_isolator.is_isolator_stable() is True

    # Unstable isolator: unstart imminent and sluggish response time
    unsafe_isolator = ScramjetIsolatorState(
        isolator_length_m=0.35,
        isolator_height_m=0.1,
        shock_train_length_m=0.35,
        combustor_to_inlet_pressure_ratio=3.5,
        isolator_stability_margin=1.00,
        response_time_ms=8.0,
        is_unstart_imminent=True
    )
    assert unsafe_isolator.is_isolator_stable() is False


def test_hypersonic_inspector_and_rubric():
    """Validates static AST inspection and 100-point rubric on canonical hypersonic core."""
    canonical_code = HypersonicReferenceLibrary.get_canonical_core()
    metrics = HypersonicInspector.inspect(canonical_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_aerothermal_heating"] is True
    assert metrics["has_real_gas_model"] is True
    assert metrics["has_isolator_stability"] is True
    assert metrics["has_telemetry_eval"] is True
    assert metrics["has_unstart_mitigation"] is True
    assert metrics["has_fatal_defects"] is False

    score, breakdown, passed, veto_reason = HypersonicRubric.evaluate(metrics)
    assert score >= 85.0
    assert passed is True
    assert veto_reason == ""
    assert breakdown["isolator_stability"] == 25.0
    assert breakdown["code_determinism"] == 15.0


def test_blind_critic_catches_flaws():
    """Validates adversarial blind critic identifying substandard isolator margin and stubs."""
    flawed_code = '''
def scramjet_flight_control(mach):
    # Weak isolator margin and poor TPS safety factor
    min_isolator_margin = 1.05
    min_tps_safety_factor = 1.15
    unstart_actuator_latency_ms = 12.0
    # TODO: add fast fuel choke and bleed door actuation
    raise NotImplementedError("unstart mitigation not wired")
'''
    critique = HypersonicBlindCritic.evaluate(flawed_code)
    assert critique["verdict"] == "REJECT"
    assert critique["passed"] is False
    assert critique["fatal_defects_count"] > 0
    assert any("Substandard scramjet isolator" in d["description"] for d in critique["defect_ledger"])


def test_elevation_engine_and_master_closed_loop():
    """Validates closed-loop elevation of flawed hypersonic code and master certification."""
    flawed_code = '''
def hypersonic_cruise(mach):
    min_isolator_margin = 1.10
    min_tps_safety_factor = 1.20
    # TODO: add real-gas chemistry
    return mach
'''
    elevation = HypersonicElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85.0
    assert "HypersonicAutonomyExecutive" in elevation["elevated_code"] or "min_isolator_margin = 1.25" in elevation["elevated_code"]

    master = ZephyrSterlingMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85.0
    assert result["verdict"] == "APPROVED"
    assert "DR. ZEPHYR STERLING — EXECUTIVE HYPERSONIC AEROTHERMODYNAMICS BRIEFING" in result["executive_briefing"]
