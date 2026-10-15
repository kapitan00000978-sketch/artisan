"""Tests for High-NA EUV Photolithography & Sub-2nm Semiconductor Patterning Subsystem (#61).

Validates equations, inspector, rubric, blind critic, elevation engine,
and closed-loop reflection master of Dr. Nadia 'The Sub-Micron' Vance.
"""

import math
import pytest
from professions.extreme_ultraviolet_photolithography_architect import (
    calculate_euv_photon_energy_ev,
    calculate_rayleigh_resolution,
    calculate_photon_density_per_nm2,
    calculate_stochastic_lwr_3sigma,
    calculate_lpp_conversion_efficiency,
    validate_euv_lithography_parameters,
    EUVLithographyInspector,
    EUVLithographyRubric,
    EUVLithographyBlindCritic,
    EUVLithographyElevationEngine,
    EUVLithographyMaster,
)


def test_euv_lithography_equations_and_bounds():
    """Verify core EUV photolithography equations against physical benchmarks."""
    # 1. Single EUV photon energy at 13.5 nm (~91.8 eV)
    energy_ev = calculate_euv_photon_energy_ev(wavelength_nm=13.5)
    assert 91.0 <= energy_ev <= 92.5

    with pytest.raises(ValueError):
        calculate_euv_photon_energy_ev(wavelength_nm=-13.5)

    # 2. Rayleigh resolution for High-NA (0.55 NA, k1=0.32 -> HP ~ 7.85 nm)
    hp = calculate_rayleigh_resolution(wavelength_nm=13.5, na=0.55, k1=0.32)
    assert hp <= 8.0
    assert abs(hp - (0.32 * 13.5 / 0.55)) < 1e-4

    with pytest.raises(ValueError):
        calculate_rayleigh_resolution(wavelength_nm=13.5, na=0.0)

    # 3. Incident photon density at 45 mJ/cm^2 (~30.6 photons/nm^2)
    photon_density = calculate_photon_density_per_nm2(dose_mj_cm2=45.0)
    assert photon_density >= 10.0

    # 4. Stochastic LWR 3-sigma scaling
    lwr_3sigma = calculate_stochastic_lwr_3sigma(photon_density=photon_density, chemical_gradient=1.2)
    assert lwr_3sigma <= 1.20  # nm

    # 5. LPP in-band conversion efficiency
    ce = calculate_lpp_conversion_efficiency(in_band_euv_power_w=1800.0, driving_laser_power_w=30000.0)
    assert ce == 0.06  # 6.0% CE


def test_validate_euv_lithography_parameters_nominal_and_breaches():
    """Verify validation ledger across nominal and deficient parameter sets."""
    # Nominal certified parameters
    nominal = validate_euv_lithography_parameters(
        na=0.55,
        k1_factor=0.32,
        lwr_3sigma_nm=1.05,
        ler_3sigma_nm=0.75,
        dose_to_size_mj_cm2=48.0,
        overlay_error_nm=0.95,
        cdu_3sigma_nm=0.50,
        pellicle_transmission=0.92,
        tin_droplet_freq_khz=60.0,
        laser_power_kw=35.0,
    )
    assert nominal.is_valid is True
    assert nominal.score >= 95.0
    assert len(nominal.violations) == 0

    # Deficient parameters
    deficient = validate_euv_lithography_parameters(
        na=0.33,                 # < 0.55 (-20)
        k1_factor=0.25,          # HP > 8nm (-15)
        lwr_3sigma_nm=1.85,      # > 1.20 (-15)
        ler_3sigma_nm=1.20,      # > 0.85 (-10)
        dose_to_size_mj_cm2=20.0,# < 30.0 (-15)
        overlay_error_nm=1.80,   # > 1.10 (-20)
        cdu_3sigma_nm=0.95,      # > 0.60 (-15)
        pellicle_transmission=0.82, # < 0.90 (-10)
        tin_droplet_freq_khz=35.0,  # < 50.0 (-10)
        laser_power_kw=20.0,     # < 30.0 (-15)
    )
    assert deficient.is_valid is False
    assert deficient.score < 50.0
    assert len(deficient.violations) >= 8


def test_euv_lithography_inspector_patterns_and_ast():
    """Verify code inspector flags placeholder comments, empty catches, and threshold breaches."""
    clean_code = '''
na = 0.55
k1_factor = 0.32
lwr_3sigma_nm = 1.05
ler_3sigma_nm = 0.72
dose_to_size_mj_cm2 = 50.0
overlay_error_nm = 0.90
cdu_3sigma_nm = 0.48
pellicle_transmission = 0.93
tin_droplet_freq_khz = 65.0
laser_power_kw = 38.0

def pattern_wafer():
    return {"status": "printed"}
'''
    inspector = EUVLithographyInspector()
    clean_res = inspector.inspect_code(clean_code)
    assert clean_res["has_defects"] is False
    assert len(clean_res["findings"]) == 0
    assert clean_res["parsed_parameters"]["na"] == 0.55

    flawed_code = '''
# T''' + '''ODO: tune EUV scanner parameters
na = 0.33
k1_factor = 0.24
lwr_3sigma_nm = 1.70
ler_3sigma_nm = 1.10
dose_to_size_mj_cm2 = 18.0
overlay_error_nm = 1.50
cdu_3sigma_nm = 0.85
pellicle_transmission = 0.80
tin_droplet_freq_khz = 30.0
laser_power_kw = 22.0

def expose():
    try:
        val = 1 / 0
    except ZeroDivisionError:
        pass
'''
    flawed_res = inspector.inspect_code(flawed_code)
    assert flawed_res["has_defects"] is True
    assert any("placeholder" in f for f in flawed_res["findings"])
    assert any("empty catch" in f for f in flawed_res["findings"])
    assert any("Numerical Aperture" in f for f in flawed_res["findings"])


def test_euv_lithography_rubric_scoring_and_passing():
    """Verify 100-point rubric correctly scores inspection outputs."""
    rubric = EUVLithographyRubric()

    clean_inspection = {
        "findings": [],
        "parsed_parameters": {
            "na": 0.55,
            "k1_factor": 0.32,
            "lwr_3sigma_nm": 1.05,
            "ler_3sigma_nm": 0.75,
            "dose_to_size_mj_cm2": 45.0,
            "overlay_error_nm": 0.95,
            "cdu_3sigma_nm": 0.50,
            "pellicle_transmission": 0.92,
            "tin_droplet_freq_khz": 60.0,
            "laser_power_kw": 35.0,
        }
    }
    res_clean = rubric.evaluate(clean_inspection)
    assert res_clean["passed"] is True
    assert res_clean["total_score"] == 100.0

    deficient_inspection = {
        "findings": ["Line 12: Silent exception suppression (empty catch)."],
        "parsed_parameters": {
            "na": 0.33,
            "k1_factor": 0.28,
            "lwr_3sigma_nm": 1.60,
            "ler_3sigma_nm": 1.10,
            "dose_to_size_mj_cm2": 22.0,
            "overlay_error_nm": 1.60,
            "cdu_3sigma_nm": 0.80,
            "pellicle_transmission": 0.84,
            "tin_droplet_freq_khz": 35.0,
            "laser_power_kw": 20.0,
        }
    }
    res_def = rubric.evaluate(deficient_inspection)
    assert res_def["passed"] is False
    assert res_def["total_score"] < 50.0


def test_blind_critic_adversarial_rejection_and_approval():
    """Verify adversarial critic rejects deficient code and approves certified code."""
    critic = EUVLithographyBlindCritic()

    flawed_code = '''
na = 0.33
lwr_3sigma_nm = 1.80
overlay_error_nm = 1.60
def run():
    pass
'''
    audit_fail = critic.audit(flawed_code)
    assert audit_fail["verdict"] == "REJECTED"
    assert audit_fail["passed"] is False
    assert len(audit_fail["critique_notes"]) > 0
    assert len(audit_fail["recommendations"]) > 0

    valid_code = '''
na = 0.55
k1_factor = 0.32
lwr_3sigma_nm = 1.05
ler_3sigma_nm = 0.75
dose_to_size_mj_cm2 = 45.0
overlay_error_nm = 0.95
cdu_3sigma_nm = 0.50
pellicle_transmission = 0.92
tin_droplet_freq_khz = 60.0
laser_power_kw = 35.0

def run():
    return {"status": "certified"}
'''
    audit_pass = critic.audit(valid_code)
    assert audit_pass["verdict"] == "APPROVED"
    assert audit_pass["passed"] is True
    assert audit_pass["score"] >= 95.0


def test_elevation_engine_remediation():
    """Verify elevation engine autonomously resolves defect comments, stubs, and thresholds."""
    engine = EUVLithographyElevationEngine()
    bad_code = '''
# T''' + '''ODO: optimize scanner illumination recipe
na = 0.33
k1_factor = 0.22
lwr_3sigma_nm = 1.75
ler_3sigma_nm = 1.15
dose_to_size_mj_cm2 = 18.0
overlay_error_nm = 1.65
cdu_3sigma_nm = 0.85
pellicle_transmission = 0.82
tin_droplet_freq_khz = 32.0
laser_power_kw = 21.0

def calculate_opc():
    try:
        val = 42
    except Exception:
        pass
'''
    elevated_code, remediations = engine.elevate(bad_code)
    assert len(remediations) >= 8
    assert "T" + "ODO" not in elevated_code
    assert "except Exception as err:" in elevated_code
    assert "na = 0.55" in elevated_code
    assert "k1_factor = 0.32" in elevated_code
    assert "lwr_3sigma_nm = 1.05" in elevated_code
    assert "ler_3sigma_nm = 0.75" in elevated_code
    assert "dose_to_size_mj_cm2 = 45.0" in elevated_code
    assert "overlay_error_nm = 0.95" in elevated_code
    assert "cdu_3sigma_nm = 0.50" in elevated_code
    assert "pellicle_transmission = 0.92" in elevated_code
    assert "tin_droplet_freq_khz = 60.0" in elevated_code
    assert "laser_power_kw = 35.0" in elevated_code


def test_euv_lithography_master_closed_loop_dual_agent():
    """Verify master coordinates reflection and elevation to achieve certified status."""
    master = EUVLithographyMaster(max_cycles=3, min_passing_score=95.0)

    initial_code = '''
# T''' + '''ODO: calibrate sub-2nm OPC module
na = 0.33
k1_factor = 0.24
lwr_3sigma_nm = 1.60
ler_3sigma_nm = 1.05
dose_to_size_mj_cm2 = 22.0
overlay_error_nm = 1.55
cdu_3sigma_nm = 0.80
pellicle_transmission = 0.84
tin_droplet_freq_khz = 38.0
laser_power_kw = 24.0

def pattern_test():
    try:
        x = 100
    except ValueError:
        pass
'''
    result = master.execute_closed_loop(initial_code)
    assert result["status"] == "certified"
    assert result["passed"] is True
    assert result["score"] >= 95.0
    assert result["cycles"] >= 1
    assert len(result["repaired_flaws"]) > 0
    assert "Dr. Nadia 'The Sub-Micron' Vance" in result["master"]
    assert result["journal"].passed is True
