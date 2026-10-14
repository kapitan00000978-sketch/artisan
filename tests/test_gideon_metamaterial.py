#!/usr/bin/env python3
"""
Unit Test Suite for Dr. Gideon 'The Refraction' Sterling
Optical Metamaterials & Transformation Optics Architect Master Subsystem
"""

import math
import cmath
import pytest
from professions.optical_metamaterial_architect import (
    complex_refractive_index,
    optical_figure_of_merit,
    dielectric_loss_tangent,
    srr_resonance_frequency,
    cylindrical_cloak_tensors,
    validate_optical_metamaterial,
    OpticalMetamaterialInspector,
    OpticalMetamaterialRubric,
    OpticalMetamaterialBlindCritic,
    OpticalMetamaterialElevationEngine,
    DrGideonSterling
)


def test_complex_refractive_index_and_figure_of_merit():
    # Double-negative medium: Re(eps) < 0 and Re(mu) < 0
    eps = -4.0 + 0.08j
    mu = -1.0 + 0.02j
    n = complex_refractive_index(eps, mu)
    # Veselago electrodynamics: Re(n) must be negative
    assert n.real < 0
    # Expected: sqrt(eps*mu) approx -2.0
    assert math.isclose(n.real, -2.0, rel_tol=0.01)

    # Figure of Merit: |Re(n)| / Im(n)
    fom = optical_figure_of_merit(n)
    assert fom > 15.0

    # Regular dielectric medium: eps > 0, mu > 0
    eps_pos = 4.0 + 0.01j
    mu_pos = 1.0 + 0.005j
    n_pos = complex_refractive_index(eps_pos, mu_pos)
    assert n_pos.real > 0


def test_dielectric_loss_tangent_and_srr_resonance():
    # Dielectric loss tangent tan(delta) = |Im(eps)| / |Re(eps)|
    eps = -2.5 + 0.05j
    loss_tan = dielectric_loss_tangent(eps)
    # 0.05 / 2.5 = 0.02
    assert math.isclose(loss_tan, 0.02, rel_tol=1e-5)

    with pytest.raises(ValueError):
        dielectric_loss_tangent(0.0 + 0.5j)

    # SRR LC resonance: L = 1.0 nH = 1e-9 H, C = 0.2533 pF = 2.533e-13 F
    l_h = 1.0e-9
    c_f = 2.533e-13
    f_res = srr_resonance_frequency(l_h, c_f)
    # f = 1 / (2 * pi * sqrt(2.533e-22)) ~ 1 / (2 * pi * 1.5915e-11) ~ 1e10 Hz (10 GHz)
    assert 9.9e9 < f_res < 10.1e9


def test_cylindrical_cloak_tensors():
    # Inner radius a = 0.1 m, outer radius b = 0.2 m, evaluate at r = 0.15 m
    r_a = 0.1
    r_b = 0.2
    r_eval = 0.15
    tensors = cylindrical_cloak_tensors(r_a, r_b, r_eval)
    # eps_r = (0.15 - 0.1) / 0.15 = 0.05 / 0.15 = 1/3
    assert math.isclose(tensors["eps_r"], 1.0 / 3.0, rel_tol=1e-5)
    # eps_theta = 0.15 / 0.05 = 3.0
    assert math.isclose(tensors["eps_theta"], 3.0, rel_tol=1e-5)
    # eps_z = (0.2 / 0.1)^2 * (1/3) = 4 * 1/3 = 4/3
    assert math.isclose(tensors["eps_z"], 4.0 / 3.0, rel_tol=1e-5)
    # det_metric = eps_r * eps_theta * eps_z = (1/3) * 3 * (4/3) = 4/3 ~ 1.333
    assert math.isclose(tensors["det_metric"], 4.0 / 3.0, rel_tol=1e-5)

    with pytest.raises(ValueError):
        cylindrical_cloak_tensors(0.2, 0.1, 0.15)
    with pytest.raises(ValueError):
        cylindrical_cloak_tensors(0.1, 0.2, 0.25)


def test_validate_optical_metamaterial():
    # Valid setup
    valid_res = validate_optical_metamaterial(
        figure_of_merit=24.5,
        loss_tangent=0.015,
        superlens_resolution_ratio=0.045,
        scattering_cross_section_ratio=0.018,
        srr_coupling_efficiency_pct=92.5,
        transformation_metric_det=0.35
    )
    assert valid_res.is_valid is True
    assert len(valid_res.violations) == 0

    # Invalid setup
    invalid_res = validate_optical_metamaterial(
        figure_of_merit=8.0,          # < 15.0
        loss_tangent=0.12,            # > 0.05
        superlens_resolution_ratio=0.35,  # > 0.10
        scattering_cross_section_ratio=0.20,  # > 0.05
        srr_coupling_efficiency_pct=65.0,     # < 85.0
        transformation_metric_det=0.02        # < 0.10
    )
    assert invalid_res.is_valid is False
    assert len(invalid_res.violations) == 6


def test_optical_metamaterial_inspector_and_rubric():
    inspector = OpticalMetamaterialInspector()

    clean_code = """
def run_metamaterial_simulation():
    figure_of_merit = 24.5
    loss_tangent = 0.015
    superlens_resolution = 0.045
    scattering_ratio = 0.018
    srr_coupling = 92.5
    metric_determinant = 0.35
    return "Negative Refraction Confirmed"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = OpticalMetamaterialRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def run_metamaterial_simulation():
    figure_of_merit = 6.0
    loss_tangent = 0.095
    superlens_resolution = 0.40
    scattering_ratio = 0.25
    srr_coupling = 60.0
    metric_determinant = 0.03
    try:
        calculate_poynting_flux()
    except Exception:
        pass
    return "Plasmonic Breakdown"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = OpticalMetamaterialRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 6
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_blind_critic_adversarial_rejection():
    critic = OpticalMetamaterialBlindCritic()
    lossy_cloak = """
def cloak_loop():
    figure_of_merit = 5.0
    loss_tangent = 0.15
    scattering_ratio = 0.30
    return "Cloak Leaking Radiation"
"""
    audit = critic.audit(lossy_cloak)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def metamaterial_cloak_executive():
    figure_of_merit = 7.5
    loss_tangent = 0.08
    superlens_resolution = 0.25
    scattering_ratio = 0.18
    srr_coupling = 70.0
    metric_determinant = 0.04
    try:
        evaluate_cloaking_boundary()
    except Exception:
        pass
    return "Unshielded Shadow"
"""
    master = DrGideonSterling(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="metamaterial_core.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Gideon" in result["master"]
    assert len(result["actions_applied"]) >= 6

    # Verify that elevated code passes inspector with 100%
    inspector = OpticalMetamaterialInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
