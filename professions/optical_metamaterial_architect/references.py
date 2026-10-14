#!/usr/bin/env python3
"""
Optical Metamaterials & Transformation Optics References
Domain Invariants: Negative-index double-negative (DNG) electrodynamics, Veselago superlens
evanescent wave amplification, Pendry transformation optics constitutive tensors,
split-ring resonator (SRR) LC resonances, and optical figure of merit (FOM).
"""

import math
import cmath
from dataclasses import dataclass, field
from typing import Dict, Any, List

SPEED_OF_LIGHT = 299792458.0  # m / s
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F / m
VACUUM_PERMEABILITY = 1.25663706212e-6  # H / m


@dataclass
class OpticalMetamaterialValidationResult:
    is_valid: bool
    figure_of_merit: float
    loss_tangent: float
    superlens_resolution_ratio: float
    scattering_cross_section_ratio: float
    srr_coupling_efficiency_pct: float
    transformation_metric_det: float
    violations: List[str] = field(default_factory=list)


def complex_refractive_index(eps: complex, mu: complex) -> complex:
    """
    Computes complex refractive index n = sqrt(eps * mu) with correct branch cut:
    For double negative media (Re(eps) < 0 and Re(mu) < 0), Re(n) < 0.
    """
    prod = eps * mu
    n_raw = cmath.sqrt(prod)
    if eps.real < 0 and mu.real < 0:
        if n_raw.real > 0:
            return -n_raw
        return n_raw
    if n_raw.real < 0:
        return -n_raw
    return n_raw


def optical_figure_of_merit(n: complex) -> float:
    """
    Computes the optical Figure of Merit (FOM) for negative index media:
    FOM = |Re(n)| / Im(n)
    """
    im_n = abs(n.imag)
    if im_n == 0:
        return float("inf")
    return abs(n.real) / im_n


def dielectric_loss_tangent(eps: complex) -> float:
    """
    Calculates dielectric/ohmic loss tangent tan(delta) = |Im(eps)| / |Re(eps)|.
    """
    re_eps = abs(eps.real)
    if re_eps == 0:
        raise ValueError("Real permittivity cannot be zero when computing loss tangent.")
    return abs(eps.imag) / re_eps


def srr_resonance_frequency(inductance_h: float, capacitance_f: float) -> float:
    """
    Computes LC magnetic resonance frequency of a split-ring resonator (SRR):
    f_0 = 1 / (2 * pi * sqrt(L * C))
    """
    if inductance_h <= 0 or capacitance_f <= 0:
        raise ValueError("Inductance and capacitance must be strictly positive.")
    return 1.0 / (2.0 * math.pi * math.sqrt(inductance_h * capacitance_f))


def cylindrical_cloak_tensors(r_inner: float, r_outer: float, r_eval: float) -> Dict[str, float]:
    """
    Computes Pendry transformation optics constitutive tensors for cylindrical cloak:
    eps_r = mu_r = (r - a) / r
    eps_theta = mu_theta = r / (r - a)
    eps_z = mu_z = (b / (b - a))^2 * (r - a) / r
    """
    if r_inner <= 0 or r_outer <= r_inner:
        raise ValueError("Inner radius must be positive and outer radius must exceed inner.")
    if not (r_inner <= r_eval <= r_outer):
        raise ValueError("Evaluation radius must be inside the cloaking shell [r_inner, r_outer].")
    
    a = r_inner
    b = r_outer
    r = r_eval

    if r == a:
        ratio = 0.0
        ratio_inv = float("inf")
    else:
        ratio = (r - a) / r
        ratio_inv = r / (r - a)

    scale_z = (b / (b - a)) ** 2
    eps_z = scale_z * ratio

    return {
        "eps_r": ratio,
        "eps_theta": ratio_inv,
        "eps_z": eps_z,
        "det_metric": ratio * ratio_inv * eps_z if ratio_inv != float("inf") else 0.0
    }


def validate_optical_metamaterial(
    figure_of_merit: float,
    loss_tangent: float,
    superlens_resolution_ratio: float,
    scattering_cross_section_ratio: float,
    srr_coupling_efficiency_pct: float,
    transformation_metric_det: float
) -> OpticalMetamaterialValidationResult:
    """
    Validates an optical metamaterial and transformation optics design against
    electrodynamic loss limits and sub-diffraction cloaking criteria.
    """
    violations = []

    # 1. Optical Figure of Merit (>= 15.0)
    if figure_of_merit < 15.0:
        violations.append(
            f"Figure of merit {figure_of_merit:.1f} < 15.0 minimum; excessive plasmonic absorption loss."
        )

    # 2. Loss Tangent (<= 0.05)
    if loss_tangent > 0.05:
        violations.append(
            f"Loss tangent {loss_tangent:.3f} > 0.05 limit; severe Joule heating and wave attenuation."
        )

    # 3. Superlens Resolution Ratio (<= 0.10 of lambda)
    if superlens_resolution_ratio > 0.10:
        violations.append(
            f"Superlens resolution {superlens_resolution_ratio:.2f} lambda > 0.10 lambda limit; fails Abbe sub-diffraction imaging."
        )

    # 4. Scattering Cross-Section Ratio (<= 0.05)
    if scattering_cross_section_ratio > 0.05:
        violations.append(
            f"Scattering cross-section ratio {scattering_cross_section_ratio:.2f} > 0.05 threshold; incomplete transformation cloaking."
        )

    # 5. SRR Coupling Efficiency (>= 85.0%)
    if srr_coupling_efficiency_pct < 85.0:
        violations.append(
            f"SRR magnetic coupling {srr_coupling_efficiency_pct:.1f}% < 85.0% threshold; insufficient artificial permeability."
        )

    # 6. Transformation Metric Determinant (>= 0.10)
    if transformation_metric_det < 0.10:
        violations.append(
            f"Metric determinant {transformation_metric_det:.2f} < 0.10 minimum; coordinate transformation singularity."
        )

    is_valid = (len(violations) == 0)
    return OpticalMetamaterialValidationResult(
        is_valid=is_valid,
        figure_of_merit=figure_of_merit,
        loss_tangent=loss_tangent,
        superlens_resolution_ratio=superlens_resolution_ratio,
        scattering_cross_section_ratio=scattering_cross_section_ratio,
        srr_coupling_efficiency_pct=srr_coupling_efficiency_pct,
        transformation_metric_det=transformation_metric_det,
        violations=violations
    )
