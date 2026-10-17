"""Test suite for Commander Jaxen Sterling - Rotating Detonation Wave Propulsion Architect.

Covers Chapman-Jouguet detonation velocities, rotating wave frequencies, pressure-gain efficiency,
aerospike nozzle performance, static and AST inspection, rubric scoring, adversarial criticism,
elevation engine, and master dual-agent closed-loop reflection.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.rotating_detonation_wave_propulsion_architect import (
    MIN_CJ_DETONATION_VELOCITY_M_S,
    MIN_CJ_PRESSURE_RATIO,
    MIN_ZND_SPIKE_PRESSURE_RATIO,
    MAX_DDT_RUNUP_DISTANCE_MM,
    MIN_DETONATION_FREQUENCY_KHZ,
    MIN_CO_ROTATING_WAVES,
    MIN_ANNULAR_GAP_MM,
    MAX_ANNULAR_GAP_MM,
    MIN_ANNULAR_DIAMETER_MM,
    MAX_ANNULAR_DIAMETER_MM,
    MIN_PRESSURE_GAIN_EFFICIENCY,
    MIN_AEROSPIKE_NOZZLE_EFFICIENCY,
    MIN_SPECIFIC_IMPULSE_S,
    MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2,
    calculate_cj_detonation_velocity,
    calculate_detonation_frequency,
    calculate_pressure_gain_ratio,
    calculate_aerospike_thrust_efficiency,
    validate_rotating_detonation_parameters,
    RotatingDetonationInspector,
    RotatingDetonationRubric,
    RotatingDetonationBlindCritic,
    RotatingDetonationElevationEngine,
    RotatingDetonationMaster,
)


def test_cj_detonation_velocity_and_frequency_models():
    """Verify Chapman-Jouguet detonation velocity and wave rotation frequency calculations."""
    # For LOX/CH4 mixture with heat release q = 6.8e6 J/kg, gamma = 1.25, R = 350 J/(kg*K), T0 = 300 K
    # 2 * (1.25^2 - 1) * 6.8e6 = 2 * 0.5625 * 6.8e6 = 7.65e6
    # 2 * 1.25 * 350 * 300 = 2.625e5
    # sum = 7.9125e6 -> sqrt = 2812.9 m/s
    v_cj = calculate_cj_detonation_velocity(6.8e6, gamma=1.25, gas_constant_r=350.0, initial_temp_k=300.0)
    assert 2750.0 <= v_cj <= 2850.0
    assert v_cj >= MIN_CJ_DETONATION_VELOCITY_M_S

    # Zero heat release edge case
    assert calculate_cj_detonation_velocity(0.0) == 0.0

    # Rotating frequency for 2 wave heads, D_annulus = 80 mm, V_cj = 2800 m/s
    # f = (2 * 2800) / (pi * 0.08) / 1000 = 5600 / 0.251327 / 1000 ~= 22.28 kHz
    freq_khz = calculate_detonation_frequency(2800.0, 80.0, num_waves=2)
    assert 21.0 <= freq_khz <= 23.5
    assert freq_khz >= MIN_DETONATION_FREQUENCY_KHZ

    # Zero diameter edge case
    assert calculate_detonation_frequency(2800.0, 0.0) == 0.0


def test_pressure_gain_and_aerospike_efficiency():
    """Verify thermodynamic pressure gain and aerospike nozzle expansion efficiency."""
    # Pressure gain: Inlet = 5.0 MPa, Exit = 5.9 MPa -> Gain = 0.18 (18%)
    gain = calculate_pressure_gain_ratio(5.9, 5.0)
    assert gain == pytest.approx(0.18, rel=1e-3)
    assert gain >= MIN_PRESSURE_GAIN_EFFICIENCY

    # Negative or zero inlet pressure edge case
    assert calculate_pressure_gain_ratio(5.0, 0.0) == 0.0

    # Aerospike nozzle efficiency across sea level (101.3 kPa) and high altitude (20.0 kPa)
    eta_sealevel = calculate_aerospike_thrust_efficiency(101.325, 101.325)
    assert eta_sealevel >= MIN_AEROSPIKE_NOZZLE_EFFICIENCY

    eta_altitude = calculate_aerospike_thrust_efficiency(20.0, 101.325)
    assert eta_altitude >= MIN_AEROSPIKE_NOZZLE_EFFICIENCY


def test_validate_rotating_detonation_parameters_nominal_and_breaches():
    """Verify validation dataclass against nominal parameters and boundary breaches."""
    # Nominal case
    res_nominal = validate_rotating_detonation_parameters(
        cj_detonation_velocity_m_s=2780.0,
        cj_pressure_ratio=22.4,
        znd_spike_pressure_ratio=42.0,
        ddt_runup_distance_mm=8.5,
        detonation_frequency_khz=28.5,
        num_co_rotating_waves=2,
        annular_channel_gap_mm=5.2,
        annular_diameter_mm=120.0,
        pressure_gain_efficiency=0.18,
        aerospike_nozzle_efficiency=0.94,
        specific_impulse_s=465.0,
        chamber_wall_heat_flux_mw_m2=24.5
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Breach case: low velocity (1800 m/s), low CJ ratio (12), low ZND (25), long DDT (25 mm), low freq (12 kHz),
    # 1 wave, narrow gap (1.5 mm), small diameter (35 mm), low gain (0.08), low nozzle eff (0.85), low Isp (380 s), high flux (45 MW/m^2)
    res_breach = validate_rotating_detonation_parameters(
        cj_detonation_velocity_m_s=1800.0,
        cj_pressure_ratio=12.0,
        znd_spike_pressure_ratio=25.0,
        ddt_runup_distance_mm=25.0,
        detonation_frequency_khz=12.0,
        num_co_rotating_waves=1,
        annular_channel_gap_mm=1.5,
        annular_diameter_mm=35.0,
        pressure_gain_efficiency=0.08,
        aerospike_nozzle_efficiency=0.85,
        specific_impulse_s=380.0,
        chamber_wall_heat_flux_mw_m2=45.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 12


def test_rotating_detonation_inspector_patterns_and_ast():
    """Verify static and AST inspection detects placeholders, deficits, and empty stubs."""
    inspector = RotatingDetonationInspector()

    flawed_code = (
        "# TODO: calibrate RDRE annular fuel manifold\n"
        "cj_detonation_velocity_m_s = 2100.0\n"
        "cj_pressure_ratio = 14.5\n"
        "znd_spike_pressure_ratio = 28.0\n"
        "ddt_runup_distance_mm = 22.0\n"
        "detonation_frequency_khz = 15.0\n"
        "num_co_rotating_waves = 1\n"
        "annular_channel_gap_mm = 1.8\n"
        "annular_diameter_mm = 40.0\n"
        "pressure_gain_efficiency = 0.09\n"
        "aerospike_nozzle_efficiency = 0.88\n"
        "specific_impulse_s = 410.0\n"
        "chamber_wall_heat_flux_mw_m2 = 42.0\n"
        "def combustor_startup() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    thrust = 1000\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "CJ_VELOCITY_DEFICIT" in flaw_ids
    assert "CJ_PRESSURE_RATIO_DEFICIT" in flaw_ids
    assert "ZND_PRESSURE_RATIO_DEFICIT" in flaw_ids
    assert "DDT_RUNUP_EXCESS" in flaw_ids
    assert "DETONATION_FREQUENCY_DEFICIT" in flaw_ids
    assert "WAVE_COUNT_DEFICIT" in flaw_ids
    assert "ANNULAR_GAP_OUT_OF_BOUNDS" in flaw_ids
    assert "ANNULAR_DIAMETER_OUT_OF_BOUNDS" in flaw_ids
    assert "PRESSURE_GAIN_DEFICIT" in flaw_ids
    assert "AEROSPIKE_EFFICIENCY_DEFICIT" in flaw_ids
    assert "SPECIFIC_IMPULSE_DEFICIT" in flaw_ids
    assert "WALL_HEAT_FLUX_EXCESS" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_rotating_detonation_rubric_scoring_and_passing():
    """Verify objective rubric scoring logic and passing thresholds."""
    rubric = RotatingDetonationRubric()

    # Zero flaws -> 100 passed
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> 75 rejected
    flaw_crit = [{"id": "CJ_VELOCITY_DEFICIT", "severity": "CRITICAL", "description": "Subsonic deflagration blowout"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> 97 passed
    flaw_low = [{"id": "TELEMETRY_SAMPLE", "severity": "LOW", "description": "Diagnostic sample"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    """Verify blind critic accurately certifies clean RDRE code and rejects flawed submissions."""
    critic = RotatingDetonationBlindCritic()

    clean_code = (
        "cj_detonation_velocity_m_s = 2780.0\n"
        "cj_pressure_ratio = 22.4\n"
        "znd_spike_pressure_ratio = 42.0\n"
        "ddt_runup_distance_mm = 8.5\n"
        "detonation_frequency_khz = 28.5\n"
        "num_co_rotating_waves = 2\n"
        "annular_channel_gap_mm = 5.2\n"
        "annular_diameter_mm = 120.0\n"
        "pressure_gain_efficiency = 0.18\n"
        "aerospike_nozzle_efficiency = 0.94\n"
        "specific_impulse_s = 465.0\n"
        "chamber_wall_heat_flux_mw_m2 = 24.5\n"
        "def combustor_startup() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "cj_detonation_velocity_m_s = 2000.0\n"
        "ddt_runup_distance_mm = 24.0\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    """Verify autonomous elevation restores code to >=95 standards and master coordinates reflection."""
    engine = RotatingDetonationElevationEngine()

    flawed_code = (
        "# TODO: optimize continuous detonation injector geometry\n"
        "cj_detonation_velocity_m_s = 2200.0\n"
        "cj_pressure_ratio = 15.0\n"
        "znd_spike_pressure_ratio = 30.0\n"
        "ddt_runup_distance_mm = 20.0\n"
        "detonation_frequency_khz = 16.0\n"
        "num_co_rotating_waves = 1\n"
        "annular_channel_gap_mm = 1.9\n"
        "annular_diameter_mm = 42.0\n"
        "pressure_gain_efficiency = 0.10\n"
        "aerospike_nozzle_efficiency = 0.89\n"
        "specific_impulse_s = 420.0\n"
        "chamber_wall_heat_flux_mw_m2 = 40.0\n"
        "def monitor_detonation() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    pressure = 100\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = RotatingDetonationBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = RotatingDetonationMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="rotating_detonation_engine.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
