"""Event Horizon General Relativistic Magnetohydrodynamics (GRMHD) Reference Equations.

Formulated by Dr. Vespera 'The Singularity' Vance,
Principal Event Horizon General Relativistic Magnetohydrodynamics (GRMHD) Architect.
"""

from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional, Tuple


# Quantitative Physical Constants & GRMHD Invariants
MIN_HORIZON_LAPSE_ALPHA: float = 0.05
MAX_DIMENSIONLESS_SPIN: float = 0.998
MIN_HORIZON_MAGNETIC_FLUX_MAD: float = 50.0
MIN_BLANDFORD_ZNAJEK_EFFICIENCY: float = 1.00
MAX_PRIMITIVE_INVERSION_TOLERANCE: float = 1.0e-10
MAX_DIV_B_ERROR: float = 1.0e-12
MAX_SYNCHROTRON_COOLING_TIME_S: float = 100.0
MAX_MAGNETOSONIC_SPEED_C: float = 1.00
MAX_MAGNETIZATION_SIGMA_FLOOR: float = 100.0
SPEED_OF_LIGHT: float = 299792458.0
GRAVITATIONAL_CONSTANT: float = 6.67430e-11
THOMSON_CROSS_SECTION: float = 6.6524587e-29
ELECTRON_MASS: float = 9.1093837e-31
VACUUM_PERMEABILITY: float = 1.25663706e-6


@dataclass
class GRMHDValidationResult:
    """Diagnostic ledger and certification report for GRMHD black hole accretion simulations."""
    is_valid: bool
    score: float
    violations: List[str] = field(default_factory=list)
    parameters: Dict[str, float] = field(default_factory=dict)
    remediation_notes: List[str] = field(default_factory=list)


def calculate_kerr_horizon_radius(
    mass_kg: float,
    dimensionless_spin: float
) -> float:
    """Calculate the outer event horizon radius r_+ for a Kerr black hole in meters.
    
    r_+ = (G * M / c^2) * (1 + sqrt(1 - a_*^2))
    """
    if mass_kg <= 0.0:
        raise ValueError("Black hole mass must be strictly positive.")
    if abs(dimensionless_spin) > 1.0:
        raise ValueError("Dimensionless spin magnitude cannot exceed 1.0 (extremal Kerr limit).")
    
    r_g = (GRAVITATIONAL_CONSTANT * mass_kg) / (SPEED_OF_LIGHT ** 2)
    discriminant = max(0.0, 1.0 - dimensionless_spin ** 2)
    r_plus = r_g * (1.0 + math.sqrt(discriminant))
    return r_plus


def calculate_blandford_znajek_luminosity(
    dimensionless_spin: float,
    magnetic_flux_webers: float,
    mass_kg: float,
    k_factor: float = 0.053
) -> float:
    """Calculate Blandford-Znajek jet extraction power in Watts.
    
    P_BZ = (k / (4*pi*c)) * Omega_H^2 * Phi_B^2
    where Omega_H = (a_* * c) / (2 * r_+)
    """
    if mass_kg <= 0.0:
        raise ValueError("Black hole mass must be strictly positive.")
    if abs(dimensionless_spin) > MAX_DIMENSIONLESS_SPIN:
        raise ValueError(f"Spin magnitude |a_*| exceeds physical Thorne equilibrium bound {MAX_DIMENSIONLESS_SPIN}.")
    
    r_plus = calculate_kerr_horizon_radius(mass_kg, dimensionless_spin)
    omega_h = (dimensionless_spin * SPEED_OF_LIGHT) / (2.0 * r_plus)
    p_bz = (k_factor / (4.0 * math.pi * SPEED_OF_LIGHT)) * (omega_h ** 2) * (magnetic_flux_webers ** 2)
    return max(0.0, p_bz)


def calculate_synchrotron_cooling_timescale(
    magnetic_field_tesla: float,
    lorentz_factor: float
) -> float:
    """Calculate the synchrotron cooling timescale tau_synch for relativistic electrons in seconds.
    
    tau_synch = (6 * pi * m_e * c) / (sigma_T * B^2 * gamma_e)
    """
    if magnetic_field_tesla <= 0.0:
        raise ValueError("Magnetic field strength must be strictly positive.")
    if lorentz_factor < 1.0:
        raise ValueError("Electron Lorentz factor gamma must be >= 1.0.")
    
    numerator = 6.0 * math.pi * ELECTRON_MASS * SPEED_OF_LIGHT
    b_energy_density = (magnetic_field_tesla ** 2) / (2.0 * VACUUM_PERMEABILITY)
    denominator = (4.0 / 3.0) * THOMSON_CROSS_SECTION * SPEED_OF_LIGHT * lorentz_factor * b_energy_density
    if denominator <= 0.0:
        return float("inf")
    return (ELECTRON_MASS * SPEED_OF_LIGHT ** 2) / (denominator)


def calculate_magnetosonic_speed(
    sound_speed_fraction_c: float,
    alfven_speed_fraction_c: float
) -> float:
    """Calculate relativistic fast magnetosonic wave speed as a fraction of c.
    
    v_ms^2 = c_s^2 + v_A^2 - c_s^2 * v_A^2  (relativistic addition)
    """
    if sound_speed_fraction_c < 0.0 or sound_speed_fraction_c >= 1.0:
        raise ValueError("Sound speed fraction c_s/c must be in [0, 1).")
    if alfven_speed_fraction_c < 0.0 or alfven_speed_fraction_c >= 1.0:
        raise ValueError("Alfven speed fraction v_A/c must be in [0, 1).")
    
    v_ms_sq = (sound_speed_fraction_c ** 2) + (alfven_speed_fraction_c ** 2) - (sound_speed_fraction_c ** 2) * (alfven_speed_fraction_c ** 2)
    return math.sqrt(min(1.0, max(0.0, v_ms_sq)))


def calculate_mad_flux_parameter(
    magnetic_flux_webers: float,
    mdot_kg_s: float,
    mass_kg: float
) -> float:
    """Calculate the dimensionless horizon magnetic flux phi_BH for MAD classification.
    
    phi_BH = Phi_B / sqrt(Mdot * r_g^2 * c)
    """
    if mdot_kg_s <= 0.0:
        raise ValueError("Accretion mass rate Mdot must be strictly positive.")
    if mass_kg <= 0.0:
        raise ValueError("Black hole mass must be strictly positive.")
    
    r_g = (GRAVITATIONAL_CONSTANT * mass_kg) / (SPEED_OF_LIGHT ** 2)
    denom = math.sqrt(mdot_kg_s * (r_g ** 2) * SPEED_OF_LIGHT)
    if denom <= 0.0:
        return 0.0
    return magnetic_flux_webers / denom


def validate_grmhd_parameters(
    lapse_alpha: float = 0.06,
    dimensionless_spin: float = 0.94,
    mad_magnetic_flux: float = 52.5,
    blandford_znajek_efficiency: float = 1.35,
    primitive_inversion_tolerance: float = 1.0e-11,
    div_b_error: float = 1.0e-13,
    synchrotron_cooling_time_s: float = 45.0,
    magnetosonic_speed_c: float = 0.88,
    magnetization_sigma: float = 75.0,
    custom_weights: Optional[Dict[str, float]] = None
) -> GRMHDValidationResult:
    """Audit and certify event horizon GRMHD parameters against relativistic physics standards."""
    params: Dict[str, float] = {
        "lapse_alpha": lapse_alpha,
        "dimensionless_spin": dimensionless_spin,
        "mad_magnetic_flux": mad_magnetic_flux,
        "blandford_znajek_efficiency": blandford_znajek_efficiency,
        "primitive_inversion_tolerance": primitive_inversion_tolerance,
        "div_b_error": div_b_error,
        "synchrotron_cooling_time_s": synchrotron_cooling_time_s,
        "magnetosonic_speed_c": magnetosonic_speed_c,
        "magnetization_sigma": magnetization_sigma,
    }

    violations: List[str] = []
    remediation_notes: List[str] = []
    deductions: float = 0.0

    # 1. 3+1 ADM Lapse Function Floor
    if lapse_alpha < MIN_HORIZON_LAPSE_ALPHA:
        violations.append(
            f"Lapse Function alpha {lapse_alpha:.4f} < {MIN_HORIZON_LAPSE_ALPHA:.4f}: "
            "Coordinate singularity breakdown in 3+1 ADM foliation near event horizon."
        )
        remediation_notes.append("Enforce minimum lapse floor alpha >= 0.05 outside Boyer-Lindquist horizon.")
        deductions += 25.0

    # 2. Black Hole Dimensionless Spin Limit
    if abs(dimensionless_spin) > MAX_DIMENSIONLESS_SPIN:
        violations.append(
            f"Black Hole Spin |a_*| {abs(dimensionless_spin):.4f} > {MAX_DIMENSIONLESS_SPIN:.4f}: "
            "Exceeds Thorne theoretical radiative equilibrium limit; risks unphysical naked singularity."
        )
        remediation_notes.append("Clamp black hole spin |a_*| <= 0.998.")
        deductions += 25.0

    # 3. Magnetically Arrested Disk (MAD) Horizon Flux
    if mad_magnetic_flux < MIN_HORIZON_MAGNETIC_FLUX_MAD:
        violations.append(
            f"MAD Horizon Magnetic Flux phi_BH {mad_magnetic_flux:.1f} < {MIN_HORIZON_MAGNETIC_FLUX_MAD:.1f}: "
            "Accretion disk in under-magnetized SANE state; fails to sustain observed relativistic jet power."
        )
        remediation_notes.append("Accumulate large-scale poloidal magnetic flux to achieve MAD state phi_BH >= 50.0.")
        deductions += 20.0

    # 4. Blandford-Znajek Jet Extraction Efficiency
    if blandford_znajek_efficiency < MIN_BLANDFORD_ZNAJEK_EFFICIENCY:
        violations.append(
            f"Blandford-Znajek Efficiency eta_BZ {blandford_znajek_efficiency:.2f} < {MIN_BLANDFORD_ZNAJEK_EFFICIENCY:.2f}: "
            "Relativistic jet engine failing to extract net spin rotational energy from Kerr black hole."
        )
        remediation_notes.append("Couple force-free jet funnel to horizon ergosphere to achieve eta_BZ >= 1.0 (100%).")
        deductions += 15.0

    # 5. Primitive Recovery Inversion Residual Tolerance
    if primitive_inversion_tolerance > MAX_PRIMITIVE_INVERSION_TOLERANCE:
        violations.append(
            f"Primitive Inversion Tolerance {primitive_inversion_tolerance:.2e} > {MAX_PRIMITIVE_INVERSION_TOLERANCE:.2e}: "
            "Conserved-to-primitive Newton-Raphson residual insufficiently constrained; causes numerical instability."
        )
        remediation_notes.append("Set 2D/1D primitive recovery inversion convergence tolerance <= 1.0e-10.")
        deductions += 20.0

    # 6. Divergence-Free Magnetic Field Constraint
    if div_b_error > MAX_DIV_B_ERROR:
        violations.append(
            f"Magnetic Field Divergence error {div_b_error:.2e} > {MAX_DIV_B_ERROR:.2e}: "
            "Magnetic monopoles generate spurious numerical Lorentz forces."
        )
        remediation_notes.append("Engage Constraint Transport (CT) or vector potential scheme to enforce div(B) <= 1.0e-12.")
        deductions += 20.0

    # 7. Synchrotron Cooling Timescale
    if synchrotron_cooling_time_s > MAX_SYNCHROTRON_COOLING_TIME_S:
        violations.append(
            f"Synchrotron Cooling Timescale {synchrotron_cooling_time_s:.1f} s > {MAX_SYNCHROTRON_COOLING_TIME_S:.1f} s: "
            "Cooling under-resolved in relativistic jet core, distorting synthetic radio/millimeter spectra."
        )
        remediation_notes.append("Enforce fast synchrotron cooling integration with tau_synch <= 100.0 s.")
        deductions += 10.0

    # 8. Relativistic Causality (Magnetosonic Speed)
    if magnetosonic_speed_c > MAX_MAGNETOSONIC_SPEED_C:
        violations.append(
            f"Magnetosonic Speed {magnetosonic_speed_c:.3f} c > {MAX_MAGNETOSONIC_SPEED_C:.3f} c: "
            "Superluminal phase speed violates Einstein causality."
        )
        remediation_notes.append("Constrain fast magnetosonic wave speed strictly sub-luminal v_ms <= 1.00 c.")
        deductions += 25.0

    # 9. Funnel Magnetization Ceiling
    if magnetization_sigma > MAX_MAGNETIZATION_SIGMA_FLOOR:
        violations.append(
            f"Funnel Magnetization sigma_M {magnetization_sigma:.1f} > {MAX_MAGNETIZATION_SIGMA_FLOOR:.1f}: "
            "Excessive magnetization floor in jet funnel causes severe numerical division-by-zero crashes."
        )
        remediation_notes.append("Apply density floor limiter to maintain funnel magnetization sigma_M <= 100.0.")
        deductions += 15.0

    score = max(0.0, 100.0 - deductions)
    is_valid = (score >= 95.0) and (len(violations) == 0)

    return GRMHDValidationResult(
        is_valid=is_valid,
        score=score,
        violations=violations,
        parameters=params,
        remediation_notes=remediation_notes
    )
