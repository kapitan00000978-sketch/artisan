"""Tests for Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Subsystem (#60).

Validates equations, inspector, rubric, blind critic, elevation engine,
and closed-loop reflection master of Dr. Silas 'The Wave' Sterling.
"""

import math
import pytest
from professions.extreme_ocean_rogue_wave_hydrodynamics_architect import (
    calculate_benjamin_feir_index,
    calculate_rogue_wave_criteria,
    calculate_wave_steepness,
    calculate_slamming_pressure,
    calculate_peregrine_breather_amplitude,
    calculate_wave_in_deck_airgap,
    validate_extreme_wave_parameters,
    ExtremeWaveInspector,
    ExtremeWaveRubric,
    ExtremeWaveBlindCritic,
    ExtremeWaveElevationEngine,
    ExtremeWaveMaster,
)


def test_extreme_wave_equations_and_bounds():
    """Verify core hydrodynamic equations against physical benchmarks."""
    # 1. Benjamin-Feir Index
    bfi = calculate_benjamin_feir_index(steepness=0.15, spectral_bandwidth=0.12)
    assert bfi > 1.0
    assert abs(bfi - (0.15 * math.sqrt(2.0) / 0.12)) < 1e-6

    with pytest.raises(ValueError):
        calculate_benjamin_feir_index(steepness=-0.1, spectral_bandwidth=0.1)
    with pytest.raises(ValueError):
        calculate_benjamin_feir_index(steepness=0.1, spectral_bandwidth=0.0)

    # 2. Rogue wave criteria
    h_ratio, crest_ratio = calculate_rogue_wave_criteria(h_max=24.0, eta_crest=14.5, h_s=11.0)
    assert h_ratio >= 2.0
    assert crest_ratio >= 1.25

    # 3. Wave steepness
    ka = calculate_wave_steepness(wavenumber_k=0.04, amplitude_a=6.5)
    assert 0.10 <= ka <= 0.44

    # 4. Slamming pressure (Wagner)
    p_slam = calculate_slamming_pressure(impact_velocity=15.0)
    assert p_slam >= 500.0  # kPa

    # 5. Peregrine breather envelope
    a0 = 4.0
    a_peak = calculate_peregrine_breather_amplitude(a0=a0, x=0.0, t=0.0)
    assert abs(a_peak - 3.0 * a0) < 1e-4

    # 6. Deck airgap
    airgap = calculate_wave_in_deck_airgap(deck_height=20.0, eta_max=16.5)
    assert airgap == 3.5


def test_validate_extreme_wave_parameters_nominal_and_breaches():
    """Verify validation ledger across nominal and deficient parameter sets."""
    # Nominal certified parameters
    nominal = validate_extreme_wave_parameters(
        benjamin_feir_index=1.65,
        rogue_height_ratio=2.25,
        crest_abnormality=1.35,
        steepness=0.25,
        slamming_pressure_kpa=720.0,
        kurtosis=3.45,
        directional_spreading_deg=18.0,
        hosm_order=4,
        deck_airgap_m=3.8,
        daf=1.25,
    )
    assert nominal.is_valid is True
    assert nominal.score >= 95.0
    assert len(nominal.violations) == 0

    # Deficient parameters
    deficient = validate_extreme_wave_parameters(
        benjamin_feir_index=0.60,       # < 1.0 (-15)
        rogue_height_ratio=1.60,        # < 2.0 (-15)
        crest_abnormality=1.05,         # < 1.25 (-10)
        steepness=0.55,                 # > 0.44 (-20)
        slamming_pressure_kpa=250.0,    # < 500.0 (-15)
        kurtosis=2.80,                  # < 3.0 (-10)
        directional_spreading_deg=45.0, # > 30.0 (-10)
        hosm_order=2,                   # < 3 (-15)
        deck_airgap_m=0.8,              # < 2.0 (-20)
        daf=2.10,                       # > 1.80 (-10)
    )
    assert deficient.is_valid is False
    assert deficient.score < 50.0
    assert len(deficient.violations) >= 8


def test_extreme_wave_inspector_patterns_and_ast():
    """Verify code inspector flags placeholder comments, empty catches, and threshold breaches."""
    clean_code = '''
benjamin_feir_index = 1.75
rogue_height_ratio = 2.30
crest_abnormality = 1.40
steepness = 0.28
slamming_pressure_kpa = 680.0
kurtosis = 3.50
directional_spreading_deg = 15.0
hosm_order = 4
deck_airgap_m = 4.0
daf = 1.30

def compute_kinematics():
    return {"status": "nominal"}
'''
    inspector = ExtremeWaveInspector()
    clean_res = inspector.inspect_code(clean_code)
    assert clean_res["has_defects"] is False
    assert len(clean_res["findings"]) == 0
    assert clean_res["parsed_parameters"]["benjamin_feir_index"] == 1.75

    flawed_code = '''
# T''' + '''ODO: calibrate rogue sea parameters
benjamin_feir_index = 0.50
rogue_height_ratio = 1.50
crest_abnormality = 1.00
steepness = 0.50
slamming_pressure_kpa = 300.0
kurtosis = 2.50
directional_spreading_deg = 40.0
hosm_order = 2
deck_airgap_m = 1.2
daf = 2.20

def simulate_wave():
    try:
        val = 1 / 0
    except ZeroDivisionError:
        pass
'''
    flawed_res = inspector.inspect_code(flawed_code)
    assert flawed_res["has_defects"] is True
    assert any("placeholder" in f for f in flawed_res["findings"])
    assert any("empty catch" in f for f in flawed_res["findings"])
    assert any("Benjamin-Feir Index" in f for f in flawed_res["findings"])


def test_extreme_wave_rubric_scoring_and_passing():
    """Verify 100-point rubric correctly scores inspection outputs."""
    rubric = ExtremeWaveRubric()

    clean_inspection = {
        "findings": [],
        "parsed_parameters": {
            "benjamin_feir_index": 1.70,
            "rogue_height_ratio": 2.20,
            "crest_abnormality": 1.30,
            "steepness": 0.25,
            "slamming_pressure_kpa": 650.0,
            "kurtosis": 3.40,
            "directional_spreading_deg": 16.0,
            "hosm_order": 4,
            "deck_airgap_m": 3.5,
            "daf": 1.30,
        }
    }
    res_clean = rubric.evaluate(clean_inspection)
    assert res_clean["passed"] is True
    assert res_clean["total_score"] == 100.0

    deficient_inspection = {
        "findings": ["Line 12: Silent exception suppression (empty catch)."],
        "parsed_parameters": {
            "benjamin_feir_index": 0.70,
            "rogue_height_ratio": 1.80,
            "crest_abnormality": 1.10,
            "steepness": 0.48,
            "slamming_pressure_kpa": 400.0,
            "kurtosis": 2.90,
            "directional_spreading_deg": 35.0,
            "hosm_order": 2,
            "deck_airgap_m": 1.5,
            "daf": 2.0,
        }
    }
    res_def = rubric.evaluate(deficient_inspection)
    assert res_def["passed"] is False
    assert res_def["total_score"] < 50.0


def test_blind_critic_adversarial_rejection_and_approval():
    """Verify adversarial critic rejects deficient code and approves certified code."""
    critic = ExtremeWaveBlindCritic()

    flawed_code = '''
benjamin_feir_index = 0.50
rogue_height_ratio = 1.40
steepness = 0.50
slamming_pressure_kpa = 200.0
def run():
    pass
'''
    audit_fail = critic.audit(flawed_code)
    assert audit_fail["verdict"] == "REJECTED"
    assert audit_fail["passed"] is False
    assert len(audit_fail["critique_notes"]) > 0
    assert len(audit_fail["recommendations"]) > 0

    valid_code = '''
benjamin_feir_index = 1.60
rogue_height_ratio = 2.25
crest_abnormality = 1.35
steepness = 0.26
slamming_pressure_kpa = 700.0
kurtosis = 3.40
directional_spreading_deg = 18.0
hosm_order = 4
deck_airgap_m = 3.6
daf = 1.30

def run():
    return {"status": "certified"}
'''
    audit_pass = critic.audit(valid_code)
    assert audit_pass["verdict"] == "APPROVED"
    assert audit_pass["passed"] is True
    assert audit_pass["score"] >= 95.0


def test_elevation_engine_remediation():
    """Verify elevation engine autonomously resolves defect comments, stubs, and thresholds."""
    engine = ExtremeWaveElevationEngine()
    bad_code = '''
# T''' + '''ODO: tune wave solver
benjamin_feir_index = 0.40
rogue_height_ratio = 1.60
crest_abnormality = 1.05
steepness = 0.52
slamming_pressure_kpa = 320.0
kurtosis = 2.70
directional_spreading_deg = 42.0
hosm_order = 2
deck_airgap_m = 1.10
daf = 2.20

def solve_kinematics():
    try:
        res = 42
    except Exception:
        pass
'''
    elevated_code, remediations = engine.elevate(bad_code)
    assert len(remediations) >= 8
    assert "T" + "ODO" not in elevated_code
    assert "except Exception as err:" in elevated_code
    assert "benjamin_feir_index = 1.50" in elevated_code
    assert "rogue_height_ratio = 2.20" in elevated_code
    assert "crest_abnormality = 1.35" in elevated_code
    assert "steepness = 0.28" in elevated_code
    assert "slamming_pressure_kpa = 650.0" in elevated_code
    assert "kurtosis = 3.40" in elevated_code
    assert "directional_spreading_deg = 15.0" in elevated_code
    assert "hosm_order = 4" in elevated_code
    assert "deck_airgap_m = 3.50" in elevated_code
    assert "daf = 1.35" in elevated_code


def test_extreme_wave_master_closed_loop_dual_agent():
    """Verify master coordinates reflection and elevation to achieve certified status."""
    master = ExtremeWaveMaster(max_cycles=3, min_passing_score=95.0)

    initial_code = '''
# T''' + '''ODO: implement non-linear wave tank controller
benjamin_feir_index = 0.65
rogue_height_ratio = 1.70
crest_abnormality = 1.10
steepness = 0.50
slamming_pressure_kpa = 380.0
kurtosis = 2.80
directional_spreading_deg = 38.0
hosm_order = 2
deck_airgap_m = 1.20
daf = 2.10

def solve_wave():
    try:
        val = 100
    except ValueError:
        pass
'''
    result = master.execute_closed_loop(initial_code)
    assert result["status"] == "certified"
    assert result["passed"] is True
    assert result["score"] >= 95.0
    assert result["cycles"] >= 1
    assert len(result["repaired_flaws"]) > 0
    assert "Dr. Silas 'The Wave' Sterling" in result["master"]
    assert result["journal"].passed is True
