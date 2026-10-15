"""Rigorous Test Suite for Master #58 Dr. Thaddeus 'The Pulse' Vance.

Pulsed Power & Terawatt Z-Pinch Plasma Confinement Architect.
Verifies magnetic pressure equations, Martin water dielectric limits, static AST/regex inspection,
100-point rubric scoring, blind critique, autonomous elevation, and master reflection engine.
"""

import pytest
from professions.pulsed_power_terawatt_plasma_architect import (
    PulsedPowerParameters,
    validate_pulsed_power_parameters,
    calculate_magnetic_pressure_mbar,
    calculate_convergence_ratio,
    calculate_stagnation_axial_field_tesla,
    calculate_water_breakdown_field_mv_cm,
    calculate_peak_electrical_power_tw,
    PulsedPowerCodeInspector,
    PulsedPowerRubricEvaluator,
    PulsedPowerBlindCritic,
    PulsedPowerElevationEngine,
    PulsedPowerMaster,
    MIN_PEAK_CURRENT_MA,
    MAX_RISE_TIME_NS,
    MIN_PEAK_POWER_TW,
    MIN_MAGNETIC_PRESSURE_MBAR,
    MIN_PRESEED_BFIELD_TESLA,
    MIN_LASER_PREHEAT_ENERGY_KJ,
    MIN_CONVERGENCE_RATIO,
    MAX_CONVERGENCE_RATIO,
    MAX_MRT_AMPLITUDE_RATIO,
    MAX_SWITCH_JITTER_NS,
)


def test_pulsed_power_equations_and_bounds():
    """Verify physical equations: magnetic pressure, convergence ratio, compressed flux, dielectric breakdown."""
    # 1. Magnetic pressure: P_mag = mu_0 * I^2 / (8 * pi^2 * r^2)
    # I = 26 MA = 2.6e7 A, r = 1.0 mm = 1.0e-3 m
    p_mag = calculate_magnetic_pressure_mbar(current_amperes=2.6e7, radius_meters=1.0e-3)
    assert p_mag > MIN_MAGNETIC_PRESSURE_MBAR
    assert 100.0 < p_mag < 120.0

    with pytest.raises(ValueError):
        calculate_magnetic_pressure_mbar(current_amperes=2.6e7, radius_meters=0.0)
    with pytest.raises(ValueError):
        calculate_magnetic_pressure_mbar(current_amperes=-10.0, radius_meters=1.0e-3)

    # 2. Convergence ratio: CR = r_0 / r_stag
    cr = calculate_convergence_ratio(initial_radius_m=3.0e-3, stagnation_radius_m=1.2e-4)
    assert cr == 25.0
    assert MIN_CONVERGENCE_RATIO <= cr <= MAX_CONVERGENCE_RATIO

    with pytest.raises(ValueError):
        calculate_convergence_ratio(initial_radius_m=1.0e-3, stagnation_radius_m=2.0e-3)

    # 3. Compressed axial magnetic field: B_stag = B_0 * CR^2 * (1 - f_loss)
    # B_0 = 15 T, CR = 20, loss = 15% -> 15 * 400 * 0.85 = 5100 T
    b_stag = calculate_stagnation_axial_field_tesla(b0_tesla=15.0, convergence_ratio=20.0, flux_loss_fraction=0.15)
    assert b_stag == 5100.0

    # 4. Martin water breakdown electric field: E_bd = 0.23 * t^-1/3 * A^-0.1
    e_bd = calculate_water_breakdown_field_mv_cm(effective_time_us=0.08, area_cm2=1000.0)
    assert e_bd > 0.10

    # 5. Peak electrical power: P = V * I (TW)
    p_tw = calculate_peak_electrical_power_tw(voltage_megavolts=3.5, current_megaamperes=25.0)
    assert p_tw == 87.5
    assert p_tw >= MIN_PEAK_POWER_TW


def test_validate_pulsed_power_parameters_nominal_and_breaches():
    """Verify validation result scoring on nominal and out-of-bounds parameters."""
    nominal_params = PulsedPowerParameters(
        peak_current_ma=26.5,
        rise_time_ns=92.0,
        peak_power_tw=88.0,
        magnetic_pressure_mbar=16.5,
        preseed_bfield_tesla=15.0,
        laser_preheat_energy_kj=2.8,
        convergence_ratio=22.0,
        mrt_amplitude_ratio=0.08,
        switch_jitter_ns=1.1,
        energy_density_kj_m3=65.0,
        stagnation_temperature_kev=3.8,
        neutron_yield=3.5e14,
    )

    result = validate_pulsed_power_parameters(nominal_params)
    assert result.is_valid is True
    assert result.score == 100.0
    assert len(result.violations) == 0
    assert result.metrics["peak_current_ma"] == 26.5

    # Severely defective parameters
    defective_params = PulsedPowerParameters(
        peak_current_ma=12.0,         # Sub-critical (<20 MA) -> -25 pts
        rise_time_ns=145.0,          # Slow rise (>100 ns) -> -20 pts
        peak_power_tw=45.0,          # Sub-terawatt (<80 TW) -> -15 pts
        magnetic_pressure_mbar=4.5,  # Sub-Mbar (<10 Mbar) -> -15 pts
        preseed_bfield_tesla=3.0,    # Weak B-field (<10 T) -> -15 pts
        laser_preheat_energy_kj=0.8, # Low preheat (<2 kJ) -> -10 pts
        convergence_ratio=42.0,      # Unstable CR (>35) -> -10 pts
        mrt_amplitude_ratio=0.35,    # High MRT (>15%) -> -10 pts
        switch_jitter_ns=4.5,        # High jitter (>2 ns) -> -10 pts
        energy_density_kj_m3=25.0,   # Low density (<50 kJ/m^3) -> -5 pts
        stagnation_temperature_kev=1.5, # Cold core (<3 keV) -> -5 pts
        neutron_yield=1.0e11,        # Low yield (<1e14) -> -5 pts
    )

    bad_result = validate_pulsed_power_parameters(defective_params)
    assert bad_result.is_valid is False
    assert bad_result.score == 0.0
    assert len(bad_result.violations) == 12


def test_pulsed_power_inspector_patterns_and_ast():
    """Verify inspector catches lazy stubs, bare excepts, empty catches, and pulsed power violations."""
    inspector = PulsedPowerCodeInspector()

    dirty_code = (
        "# " + "TODO: wire up laser pre-heat timing\n"
        "peak_current = 14.0\n"
        "rise_time = 125.0\n"
        "peak_power = 50.0\n"
        "magnetic_pressure = 4.0\n"
        "preseed_bfield = 5.0\n"
        "laser_preheat = 1.0\n"
        "switch_jitter = 3.5\n"
        "mrt_amplitude_ratio = 0.28\n"
        "unmagnetized_pinch = True\n"
        "def trigger_ltd_cavity():\n"
        "    pass\n"
        "try:\n"
        "    fire_pulse()\n"
        "except:\n"
        "    pass\n"
    )

    findings = inspector.inspect_source(dirty_code)
    finding_types = [f["type"] for f in findings]

    assert "LAZY_STUB" in finding_types
    assert "SUB_CRITICAL_DISCHARGE_CURRENT" in finding_types
    assert "SLOW_CURRENT_RISE_TIME" in finding_types
    assert "SUB_TERAWATT_POWER" in finding_types
    assert "SUB_MEGABAR_PRESSURE" in finding_types
    assert "INSUFFICIENT_PRESEED_BFIELD" in finding_types
    assert "INSUFFICIENT_LASER_PREHEAT" in finding_types
    assert "EXCESSIVE_SWITCH_JITTER" in finding_types
    assert "EXCESSIVE_MRT_GROWTH" in finding_types
    assert "UNMAGNETIZED_PINCH_MODE" in finding_types
    assert "EMPTY_FUNCTION_STUB" in finding_types
    assert "BARE_EXCEPT" in finding_types
    assert "SILENT_PASS_EXCEPT" in finding_types


def test_pulsed_power_rubric_scoring_and_passing():
    """Verify rubric scoring across 4 dimensions and 95.0 passing threshold."""
    evaluator = PulsedPowerRubricEvaluator()

    # Clean findings -> 100/100
    clean_report = evaluator.evaluate(findings=[], metrics={})
    assert clean_report.is_passing is True
    assert clean_report.total_score == 100.0
    assert "PASSED" in clean_report.summary

    # Defective findings -> fails 95.0 threshold
    flawed_findings = [
        {"type": "SUB_CRITICAL_DISCHARGE_CURRENT", "message": "Peak current 15.0 MA < 20.0 MA"},
        {"type": "LAZY_STUB", "message": "stub comment"},
    ]
    flawed_report = evaluator.evaluate(flawed_findings, metrics={})
    assert flawed_report.is_passing is False
    assert flawed_report.total_score <= 70.0
    assert "REJECTED" in flawed_report.summary


def test_blind_critic_adversarial_rejection_and_approval():
    """Verify Blind Critic rejects defective code and certifies production-grade code."""
    critic = PulsedPowerBlindCritic()

    bad_code = (
        "# " + "FIXME: MRT instability disrupts liner\n"
        "peak_current = 10.0\n"
        "rise_time = 150.0\n"
        "def simulate_pinch():\n"
        "    pass\n"
    )

    verdict_bad = critic.audit(bad_code)
    assert verdict_bad.verdict == "REJECTED_DEFECTIVE"
    assert verdict_bad.passed is False
    assert verdict_bad.score < 95.0
    assert len(verdict_bad.remediation_plan) > 0

    clean_code = (
        "'''Pulsed power Magnetized Liner Inertial Fusion simulation.'''\n"
        "import logging\n\n"
        "def compute_pinch_stagnation() -> dict:\n"
        "    peak_current = 26.0\n"
        "    rise_time = 95.0\n"
        "    peak_power = 85.0\n"
        "    magnetic_pressure = 15.0\n"
        "    preseed_bfield = 15.0\n"
        "    laser_preheat = 2.5\n"
        "    switch_jitter = 1.2\n"
        "    mrt_amplitude_ratio = 0.08\n"
        "    return {'status': 'nominal', 'I_peak': peak_current}\n"
    )

    verdict_clean = critic.audit(clean_code)
    assert verdict_clean.verdict == "CERTIFIED_WORLD_CLASS"
    assert verdict_clean.passed is True
    assert verdict_clean.score >= 95.0


def test_elevation_engine_remediation():
    """Verify Elevation Engine automatically eliminates stubs and restores MagLIF parameters."""
    engine = PulsedPowerElevationEngine()

    flawed_source = (
        "# " + "TODO: resolve switch jitter and MRT bubble growth\n"
        "unmagnetized_pinch = True\n"
        "disable_axial_bfield = True\n"
        "peak_current = 12.0\n"
        "rise_time = 135.0\n"
        "peak_power = 55.0\n"
        "magnetic_pressure = 5.0\n"
        "preseed_bfield = 4.0\n"
        "laser_preheat = 1.1\n"
        "switch_jitter = 3.2\n"
        "mrt_amplitude_ratio = 0.25\n"
        "def discharge_stage() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    trigger_pulse()\n"
        "except:\n"
        "    pass\n"
    )

    elevated, stats = engine.elevate(flawed_source)

    assert stats["stubs_removed"] >= 1
    assert stats["maglif_restored"] >= 2
    assert stats["parameters_elevated"] >= 8
    assert stats["empty_stubs_filled"] >= 1
    assert stats["exceptions_remediated"] >= 1

    # Verify remediated values
    assert "peak_current = 26.0" in elevated
    assert "rise_time = 95.0" in elevated
    assert "peak_power = 85.0" in elevated
    assert "magnetic_pressure = 15.0" in elevated
    assert "preseed_bfield = 15.0" in elevated
    assert "laser_preheat = 2.5" in elevated
    assert "switch_jitter = 1.2" in elevated
    assert "mrt_amplitude_ratio = 0.08" in elevated
    assert "unmagnetized_pinch = False" in elevated
    assert "pass" not in elevated


def test_pulsed_power_master_closed_loop_dual_agent():
    """Verify Master orchestrates closed-loop audit, elevation, and journal recording."""
    class MockJournal:
        def __init__(self):
            self.records = []

        def record_decision(self, iteration, target, flaws, actions, score_before, score_after):
            self.records.append({
                "iteration": iteration,
                "target": target,
                "flaws": flaws,
                "actions": actions,
                "score_before": score_before,
                "score_after": score_after,
            })

    journal = MockJournal()
    master = PulsedPowerMaster(journal=journal)

    defective_code = (
        "# " + "TODO: fix slow current delivery\n"
        "peak_current = 15.0\n"
        "rise_time = 120.0\n"
        "preseed_bfield = 5.0\n"
        "def fire_zpinch() -> dict:\n"
        "    pass\n"
    )

    result = master.evaluate_and_elevate(defective_code, target_file="zpinch_drive.py")

    assert result["status"] == "certified"
    assert result["final_score"] >= 95.0
    assert result["iterations"] >= 1
    assert len(result["repaired_flaws"]) > 0
    assert len(journal.records) >= 1
    assert journal.records[0]["score_after"] >= 95.0
