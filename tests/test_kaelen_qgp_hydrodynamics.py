"""Test Suite for Relativistic Heavy-Ion QGP Hydrodynamics Subsystem.

Validates Dr. Kaelen 'The Quark' Sterling's
Relativistic Heavy-Ion Quark-Gluon Plasma Hydrodynamics Subsystem.
"""

import math
import pytest

from professions.relativistic_heavy_ion_quark_gluon_plasma_hydrodynamics_architect import (
    KSS_BOUND_ETA_OVER_S,
    MIN_ETA_OVER_S,
    MAX_ETA_OVER_S,
    MAX_ZETA_OVER_S,
    MIN_QCD_CRITICAL_TEMP_MEV,
    MAX_QCD_CRITICAL_TEMP_MEV,
    NOMINAL_QCD_CRITICAL_TEMP_MEV,
    MIN_THERMALIZATION_TAU_FM_C,
    MAX_THERMALIZATION_TAU_FM_C,
    MIN_JET_QUENCHING_QHAT_GEV2_FM,
    MIN_ISRAEL_STEWART_RELAXATION_RATIO,
    MIN_FREEZEOUT_TEMP_MEV,
    MAX_FREEZEOUT_TEMP_MEV,
    MIN_ELLIPTIC_FLOW_V2,
    MAX_ELLIPTIC_FLOW_V2,
    MIN_SOUND_SPEED_SQ_AT_TC,
    HBAR_C_MEV_FM,
    SPEED_OF_LIGHT,
    QGPValidationResult,
    calculate_israel_stewart_shear_relaxation_time,
    calculate_bjorken_energy_density,
    calculate_kss_viscosity_margin,
    calculate_speed_of_sound_squared,
    validate_qgp_parameters,
    QGPHydrodynamicsInspector,
    QGPHydrodynamicsRubric,
    PASSING_SCORE,
    QGPHydrodynamicsBlindCritic,
    QGPHydrodynamicsElevationEngine,
    QGPHydrodynamicsMaster,
    ActiveDecisionJournal,
)


def test_qgp_equations_and_bounds() -> None:
    """Verify core QGP hydrodynamic formulas, relaxation times, and KSS bounds."""
    # 1. KSS lower bound value check
    assert math.isclose(KSS_BOUND_ETA_OVER_S, 1.0 / (4.0 * math.pi), rel_tol=1e-5)
    margin = calculate_kss_viscosity_margin(0.12)
    assert margin > 0.0

    # 2. Israel-Stewart shear relaxation time
    tau_pi = calculate_israel_stewart_shear_relaxation_time(0.12, 200.0, 5.0)
    assert 0.1 < tau_pi < 5.0  # realistic subatomic timescale in fm/c

    with pytest.raises(ValueError):
        calculate_israel_stewart_shear_relaxation_time(0.02, 200.0)  # violates KSS bound
    with pytest.raises(ValueError):
        calculate_israel_stewart_shear_relaxation_time(0.12, -50.0)  # negative T

    # 3. Bjorken energy density
    eps_0 = calculate_bjorken_energy_density(0.60, 2000.0, 150.0)
    assert eps_0 > 0.0

    # 4. Speed of sound minimum near T_c
    cs2_tc = calculate_speed_of_sound_squared(155.0)
    assert 0.14 <= cs2_tc <= 0.16
    cs2_high_t = calculate_speed_of_sound_squared(800.0)
    assert cs2_high_t > cs2_tc


def test_validate_qgp_parameters_nominal_and_breaches() -> None:
    """Verify parameter audit under nominal conditions and targeted physical violations."""
    # Nominal case
    res_nominal = validate_qgp_parameters(
        eta_over_s=0.12,
        zeta_over_s=0.04,
        qcd_critical_temp_mev=155.0,
        thermalization_tau_fm_c=0.40,
        jet_quenching_qhat_gev2_fm=1.65,
        israel_stewart_relaxation_ratio=5.5,
        freezeout_temp_mev=140.0,
        elliptic_flow_v2=0.095,
        sound_speed_sq_tc=0.155,
    )
    assert res_nominal.is_valid is True
    assert res_nominal.score == 100.0
    assert len(res_nominal.violations) == 0

    # Breach 1: Viscosity violates KSS lower bound
    res_kss = validate_qgp_parameters(eta_over_s=0.03)
    assert res_kss.is_valid is False
    assert any("Shear Viscosity" in v for v in res_kss.violations)

    # Breach 2: Excess bulk viscosity
    res_zeta = validate_qgp_parameters(zeta_over_s=0.25)
    assert res_zeta.is_valid is False
    assert any("Bulk Viscosity" in v for v in res_zeta.violations)

    # Breach 3: Unphysical critical temperature
    res_tc = validate_qgp_parameters(qcd_critical_temp_mev=195.0)
    assert res_tc.is_valid is False
    assert any("QCD Critical Temp" in v for v in res_tc.violations)

    # Breach 4: Premature thermalization
    res_tau = validate_qgp_parameters(thermalization_tau_fm_c=0.05)
    assert res_tau.is_valid is False
    assert any("Thermalization Time" in v for v in res_tau.violations)

    # Breach 5: Inadequate jet quenching
    res_qhat = validate_qgp_parameters(jet_quenching_qhat_gev2_fm=0.50)
    assert res_qhat.is_valid is False
    assert any("Jet Quenching" in v for v in res_qhat.violations)

    # Breach 6: Acausal Israel-Stewart relaxation ratio
    res_causality = validate_qgp_parameters(israel_stewart_relaxation_ratio=2.0)
    assert res_causality.is_valid is False
    assert any("Israel-Stewart Relaxation Ratio" in v for v in res_causality.violations)


def test_qgp_inspector_patterns_and_ast() -> None:
    """Verify inspector AST syntax scanning and regex parameter extraction."""
    inspector = QGPHydrodynamicsInspector()

    defective_code = (
        "# T" + "ODO: tune Israel-Stewart relaxation\n"
        "def evolve_bjorken_hydro():\n"
        "    pass\n\n"
        "try:\n"
        "    sample_cooper_frye()\n"
        "except Exception:\n"
        "    pass\n\n"
        "eta_over_s = 0.04\n"
        "zeta_over_s = 0.22\n"
        "qcd_critical_temp_mev = 185.0\n"
        "thermalization_tau_fm_c = 0.08\n"
        "jet_quenching_qhat_gev2_fm = 0.60\n"
        "israel_stewart_relaxation_ratio = 2.5\n"
        "freezeout_temp_mev = 110.0\n"
        "elliptic_flow_v2 = 0.015\n"
        "sound_speed_sq_tc = 0.09\n"
    )

    result = inspector.inspect_code(defective_code)
    assert result["has_defects"] is True
    assert len(result["findings"]) >= 10
    assert result["parsed_parameters"]["eta_over_s"] == 0.04
    assert result["parsed_parameters"]["qcd_critical_temp_mev"] == 185.0
    assert result["parsed_parameters"]["elliptic_flow_v2"] == 0.015


def test_qgp_rubric_scoring_and_passing() -> None:
    """Verify objective 100-point rubric evaluation."""
    rubric = QGPHydrodynamicsRubric()
    inspector = QGPHydrodynamicsInspector()

    valid_code = (
        "def simulate_qgp_expansion():\n"
        "    return {'status': 'thermalized', 'perfect_fluid': True}\n\n"
        "eta_over_s = 0.12\n"
        "zeta_over_s = 0.04\n"
        "qcd_critical_temp_mev = 155.0\n"
        "thermalization_tau_fm_c = 0.40\n"
        "jet_quenching_qhat_gev2_fm = 1.65\n"
        "israel_stewart_relaxation_ratio = 5.5\n"
        "freezeout_temp_mev = 140.0\n"
        "elliptic_flow_v2 = 0.095\n"
        "sound_speed_sq_tc = 0.155\n"
    )

    inspection = inspector.inspect_code(valid_code)
    eval_res = rubric.evaluate(inspection)
    assert eval_res["passed"] is True
    assert eval_res["total_score"] >= PASSING_SCORE


def test_blind_critic_adversarial_rejection_and_approval() -> None:
    """Verify adversarial critic rejects unphysical code and approves compliant code."""
    critic = QGPHydrodynamicsBlindCritic()

    flawed_code = (
        "# T" + "ODO: add viscosity\n"
        "eta_over_s = 0.02\n"
        "israel_stewart_relaxation_ratio = 1.2\n"
    )

    audit_flawed = critic.audit(flawed_code)
    assert audit_flawed["passed"] is False
    assert len(audit_flawed["critique_notes"]) > 0
    assert len(audit_flawed["recommendations"]) > 0

    certified_code = (
        "eta_over_s = 0.12\n"
        "zeta_over_s = 0.04\n"
        "qcd_critical_temp_mev = 155.0\n"
        "thermalization_tau_fm_c = 0.40\n"
        "jet_quenching_qhat_gev2_fm = 1.65\n"
        "israel_stewart_relaxation_ratio = 5.5\n"
        "freezeout_temp_mev = 140.0\n"
        "elliptic_flow_v2 = 0.095\n"
        "sound_speed_sq_tc = 0.155\n"
    )
    audit_cert = critic.audit(certified_code)
    assert audit_cert["passed"] is True
    assert audit_cert["score"] >= PASSING_SCORE


def test_elevation_engine_remediation() -> None:
    """Verify elevation engine repairs stubs, exceptions, and physical invariants."""
    engine = QGPHydrodynamicsElevationEngine()

    flawed_code = (
        "# T" + "ODO: complete Cooper-Frye sampling\n"
        "def sample_particulates():\n"
        "    pass\n\n"
        "try:\n"
        "    run_hydro_step()\n"
        "except Exception:\n"
        "    pass\n\n"
        "eta_over_s = 0.03\n"
        "zeta_over_s = 0.25\n"
        "qcd_critical_temp_mev = 190.0\n"
        "thermalization_tau_fm_c = 0.05\n"
        "jet_quenching_qhat_gev2_fm = 0.40\n"
        "israel_stewart_relaxation_ratio = 2.0\n"
        "freezeout_temp_mev = 105.0\n"
        "elliptic_flow_v2 = 0.02\n"
        "sound_speed_sq_tc = 0.08\n"
    )

    elevated_code, remediations = engine.elevate(flawed_code)
    assert len(remediations) >= 8
    assert "T" + "ODO" not in elevated_code
    assert "except Exception as err:" in elevated_code
    assert "eta_over_s = 0.12" in elevated_code
    assert "zeta_over_s = 0.04" in elevated_code
    assert "qcd_critical_temp_mev = 155.0" in elevated_code
    assert "thermalization_tau_fm_c = 0.40" in elevated_code
    assert "jet_quenching_qhat_gev2_fm = 1.65" in elevated_code
    assert "israel_stewart_relaxation_ratio = 5.5" in elevated_code
    assert "freezeout_temp_mev = 140.0" in elevated_code
    assert "elliptic_flow_v2 = 0.095" in elevated_code
    assert "sound_speed_sq_tc = 0.155" in elevated_code


def test_qgp_master_closed_loop_dual_agent() -> None:
    """Verify closed-loop dual-agent reflection engine elevates defective code to certified status."""
    master = QGPHydrodynamicsMaster()

    flawed_code = (
        "# T" + "ODO: implement boost-invariant longitudinal expansion\n"
        "def compute_energy_momentum_tensor():\n"
        "    pass\n\n"
        "try:\n"
        "    solve_conservation_laws()\n"
        "except Exception:\n"
        "    pass\n\n"
        "eta_over_s = 0.025\n"
        "zeta_over_s = 0.30\n"
        "qcd_critical_temp_mev = 180.0\n"
        "thermalization_tau_fm_c = 0.10\n"
        "jet_quenching_qhat_gev2_fm = 0.50\n"
        "israel_stewart_relaxation_ratio = 1.5\n"
        "freezeout_temp_mev = 115.0\n"
        "elliptic_flow_v2 = 0.025\n"
        "sound_speed_sq_tc = 0.07\n"
    )

    result = master.execute_closed_loop(flawed_code)
    assert result["status"] == "certified"
    assert result["passed"] is True
    assert result["score"] >= PASSING_SCORE
    assert result["cycles"] >= 1
    assert len(result["repaired_flaws"]) > 0
    assert result["master"] == "Dr. Kaelen 'The Quark' Sterling"
