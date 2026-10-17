"""Test suite for Dr. Morwenna Sterling - Closed-Loop ECLSS & Bioregenerative Space Architect.

Covers stoichiometric chemical models, life support validation, AST inspection, rubric, critic, elevation, and master reflection.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from professions.closed_loop_ecological_life_support_architect import (
    MOLAR_MASS_CO2,
    MOLAR_MASS_H2,
    MOLAR_MASS_H2O,
    MOLAR_MASS_O2,
    MOLAR_MASS_CH4,
    MIN_SABATIER_EFFICIENCY,
    MIN_ELECTROLYSIS_EFFICIENCY,
    MIN_WATER_LOOP_RECOVERY,
    MAX_PERMEATE_TOC_UG_PER_L,
    calculate_sabatier_yield,
    calculate_electrolysis_yield,
    calculate_photobioreactor_o2_output,
    calculate_water_recovery_balance,
    validate_eclss_parameters,
    ECLSSInspector,
    ECLSSRubric,
    ECLSSBlindCritic,
    ECLSSElevationEngine,
    ECLSSMaster,
)


def test_sabatier_and_electrolysis_stoichiometry():
    # 100 kg CO2 with 85% efficiency
    m_h2o, m_ch4, m_h2_req = calculate_sabatier_yield(100.0, efficiency=0.85)
    # Expected: m_h2o ~= 100 * 0.85 * (36.03 / 44.01) = 69.589 kg
    assert 69.0 <= m_h2o <= 70.0
    # Expected: m_ch4 ~= 100 * 0.85 * (16.043 / 44.01) = 30.983 kg
    assert 30.5 <= m_ch4 <= 31.5
    # Expected: m_h2_req ~= 100 * 0.85 * (8.064 / 44.01) = 15.576 kg
    assert 15.0 <= m_h2_req <= 16.0

    # PEM Water electrolysis: 100 kg H2O with 80% efficiency
    m_o2, m_h2 = calculate_electrolysis_yield(100.0, efficiency=0.80)
    # Expected: m_o2 ~= 100 * 0.80 * (31.9988 / 36.03) = 71.05 kg
    assert 70.5 <= m_o2 <= 71.5
    # Expected: m_h2 ~= 100 * 0.80 * (4.032 / 36.03) = 8.95 kg
    assert 8.5 <= m_h2 <= 9.5

    # Zero or negative inputs
    assert calculate_sabatier_yield(0.0) == (0.0, 0.0, 0.0)
    assert calculate_electrolysis_yield(-10.0) == (0.0, 0.0)


def test_photobioreactor_o2_output_and_water_recovery():
    # 44.01 kg CO2 (1000 moles) with PQ = 1.15
    # 1000 moles CO2 -> 1150 moles O2 * 0.0319988 kg/mol = 36.798 kg O2
    o2_gen = calculate_photobioreactor_o2_output(44.01, photosynthetic_quotient=1.15)
    assert 36.5 <= o2_gen <= 37.0

    # Water recovery: 500 liters graywater with 98.5% recovery
    potable, brine = calculate_water_recovery_balance(500.0, recovery_fraction=0.985)
    assert potable == pytest.approx(492.5)
    assert brine == pytest.approx(7.5)


def test_validate_eclss_parameters_nominal_and_breaches():
    # Nominal parameters
    res_nominal = validate_eclss_parameters(
        sabatier_efficiency=0.88,
        electrolysis_efficiency=0.85,
        water_recovery_fraction=0.985,
        permeate_toc_ug_per_l=350.0,
        crew_o2_rate_kg_day=0.84,
        crew_co2_rate_kg_day=1.00,
        photosynthetic_quotient=1.15,
        algal_growth_rate_hr=0.065,
        cabin_pressure_kpa=101.3,
        cabin_po2_kpa=21.0,
        cabin_pco2_kpa=0.30,
        catalytic_temp_c=425.0
    )
    assert res_nominal.is_valid is True
    assert len(res_nominal.flaws) == 0

    # Multiple critical breaches: low Sabatier eff, low water recovery, high TOC, high cabin pCO2
    res_breach = validate_eclss_parameters(
        sabatier_efficiency=0.60,
        electrolysis_efficiency=0.70,
        water_recovery_fraction=0.90,
        permeate_toc_ug_per_l=850.0,
        crew_o2_rate_kg_day=0.50,
        crew_co2_rate_kg_day=1.50,
        photosynthetic_quotient=0.90,
        algal_growth_rate_hr=0.02,
        cabin_pressure_kpa=55.0,
        cabin_po2_kpa=14.0,
        cabin_pco2_kpa=0.85,
        catalytic_temp_c=250.0
    )
    assert res_breach.is_valid is False
    assert len(res_breach.flaws) == 12


def test_eclss_inspector_patterns_and_ast():
    inspector = ECLSSInspector()

    flawed_code = (
        "# TODO: finish life support sizing\n"
        "sabatier_efficiency = 0.65\n"
        "water_recovery_fraction = 0.92\n"
        "permeate_toc_ug_per_l = 750.0\n"
        "cabin_pco2_kpa = 0.65\n"
        "catalytic_temp_c = 310.0\n"
        "def pump_water() -> bool:\n"
        "    pass\n"
        "try:\n"
        "    val = 1\n"
        "except Exception:\n"
        "    pass\n"
    )

    flaws = inspector.inspect_source(flawed_code)
    flaw_ids = [f["id"] for f in flaws]

    assert "LAZY_TODO_COMMENT" in flaw_ids
    assert "SABATIER_EFFICIENCY_DEFICIT" in flaw_ids
    assert "WATER_RECOVERY_DEFICIT" in flaw_ids
    assert "PERMEATE_TOC_CONTAMINATION" in flaw_ids
    assert "CABIN_HYPERCAPNIA_RISK" in flaw_ids
    assert "CATALYTIC_OXIDIZER_COLD" in flaw_ids
    assert "EMPTY_FUNCTION_BODY" in flaw_ids
    assert "EMPTY_EXCEPT_BLOCK" in flaw_ids

    text_flaws = inspector.inspect_code(flawed_code)
    assert len(text_flaws) == len(flaws)


def test_eclss_rubric_scoring_and_passing():
    rubric = ECLSSRubric()

    # Zero flaws
    eval_pass = rubric.evaluate([])
    assert eval_pass.score == 100
    assert eval_pass.passed is True

    # One CRITICAL flaw (-25 pts) -> score 75, rejected
    flaw_crit = [{"id": "SABATIER_EFFICIENCY_DEFICIT", "severity": "CRITICAL", "description": "Breach"}]
    eval_crit = rubric.evaluate(flaw_crit)
    assert eval_crit.score == 75
    assert eval_crit.passed is False

    # One LOW flaw (-3 pts) -> score 97, passes (>= 95)
    flaw_low = [{"id": "LOG_NOTE", "severity": "LOW", "description": "Minor note"}]
    eval_low = rubric.evaluate(flaw_low)
    assert eval_low.score == 97
    assert eval_low.passed is True


def test_blind_critic_adversarial_rejection():
    critic = ECLSSBlindCritic()

    clean_code = (
        "sabatier_efficiency = 0.88\n"
        "electrolysis_efficiency = 0.85\n"
        "water_recovery_fraction = 0.985\n"
        "permeate_toc_ug_per_l = 350.0\n"
        "crew_o2_rate_kg_day = 0.84\n"
        "crew_co2_rate_kg_day = 1.00\n"
        "photosynthetic_quotient = 1.15\n"
        "algal_growth_rate_hr = 0.065\n"
        "cabin_pressure_kpa = 101.3\n"
        "cabin_po2_kpa = 21.0\n"
        "cabin_pco2_kpa = 0.30\n"
        "catalytic_temp_c = 425.0\n"
        "def run_loop() -> bool:\n"
        "    return True\n"
    )

    clean_res = critic.audit(clean_code)
    assert clean_res["verdict"] == "APPROVED"
    assert clean_res["score"] == 100
    assert clean_res["passed"] is True

    flawed_code = (
        "sabatier_efficiency = 0.65\n"
        "water_recovery_fraction = 0.90\n"
    )
    flawed_res = critic.audit(flawed_code)
    assert flawed_res["verdict"] == "REJECTED"
    assert flawed_res["passed"] is False
    assert flawed_res["score"] < 95


def test_elevation_engine_and_master_closed_loop():
    engine = ECLSSElevationEngine()

    flawed_code = (
        "# TODO: optimize reactor\n"
        "sabatier_efficiency = 0.65\n"
        "electrolysis_efficiency = 0.70\n"
        "water_recovery_fraction = 0.92\n"
        "permeate_toc_ug_per_l = 650.0\n"
        "crew_o2_rate_kg_day = 0.50\n"
        "crew_co2_rate_kg_day = 1.60\n"
        "photosynthetic_quotient = 0.90\n"
        "algal_growth_rate_hr = 0.02\n"
        "cabin_pressure_kpa = 55.0\n"
        "cabin_po2_kpa = 14.0\n"
        "cabin_pco2_kpa = 0.65\n"
        "catalytic_temp_c = 320.0\n"
        "def telemetry() -> dict:\n"
        "    pass\n"
        "try:\n"
        "    x = 10\n"
        "except ValueError:\n"
        "    pass\n"
    )

    elevated, actions = engine.elevate(flawed_code)
    assert len(actions) > 0

    critic = ECLSSBlindCritic()
    audit_after = critic.audit(elevated)
    assert audit_after["passed"] is True
    assert audit_after["score"] >= 95

    # Test master closed-loop execution
    master = ECLSSMaster()
    res = master.evaluate_and_elevate(flawed_code, target_file="life_support_loop.py")
    assert res["status"] == "certified"
    assert res["final_score"] >= 95
    assert res["iterations"] >= 1
    assert len(res["repaired_flaws"]) > 0
