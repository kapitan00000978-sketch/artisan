#!/usr/bin/env python3
"""
Astrodynamics & Interplanetary Trajectory Mathematical References
Domain Invariants: Patched conics, Tisserand parameter, CR3BP Jacobi constant, SRP perturbation.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

# Standard Gravitational Parameters (km^3 / s^2)
MU_SUN = 1.32712440018e11
MU_EARTH = 3.986004418e5
MU_MARS = 4.282837e4
MU_JUPITER = 1.26686534e8

# Astronomical Unit (km)
AU_KM = 1.495978707e8

# Solar radiation constant at 1 AU (N / m^2)
SOLAR_FLUX_P0 = 4.56e-6


@dataclass
class TrajectoryValidationResult:
    is_valid: bool
    delta_v_total: float
    propellant_margin_sf: float
    tisserand_error: float
    periapsis_clearance_km: float
    jacobi_constant: float
    srp_drift_accel: float
    violations: List[str] = field(default_factory=list)


def vis_viva_velocity(mu: float, r: float, a: float) -> float:
    """
    Computes orbital speed using the vis-viva equation:
    v = sqrt(mu * (2/r - 1/a))
    """
    if r <= 0:
        raise ValueError(f"Radius r must be strictly positive, got {r}")
    term = (2.0 / r) - (1.0 / a)
    if term < 0:
        raise ValueError(f"Hyperbolic or unphysical orbit parameters: 2/r - 1/a = {term}")
    return math.sqrt(mu * term)


def hohmann_transfer_delta_v(mu: float, r1: float, r2: float) -> Tuple[float, float, float]:
    """
    Calculates Hohmann transfer delta-v between circular coplanar orbits.
    Returns (delta_v1, delta_v2, total_delta_v).
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbital radii r1 and r2 must be strictly positive.")
    a_tx = (r1 + r2) / 2.0
    v1 = math.sqrt(mu / r1)
    v2 = math.sqrt(mu / r2)
    v_tx1 = math.sqrt(mu * ((2.0 / r1) - (1.0 / a_tx)))
    v_tx2 = math.sqrt(mu * ((2.0 / r2) - (1.0 / a_tx)))
    
    dv1 = abs(v_tx1 - v1)
    dv2 = abs(v2 - v_tx2)
    return dv1, dv2, dv1 + dv2


def tisserand_parameter(a: float, e: float, inc_rad: float, a_planet: float) -> float:
    """
    Calculates the Tisserand parameter with respect to a perturbing planet:
    T_p = (a_planet / a) + 2 * sqrt((a / a_planet) * (1 - e^2)) * cos(i)
    """
    if a <= 0 or a_planet <= 0:
        raise ValueError("Semimajor axes must be strictly positive.")
    if e >= 1.0 or e < 0.0:
        raise ValueError(f"Eccentricity must be in [0, 1) for elliptic orbits, got {e}")
    term_sqrt = (a / a_planet) * (1.0 - e * e)
    if term_sqrt < 0:
        raise ValueError("Unphysical eccentricity configuration.")
    return (a_planet / a) + 2.0 * math.sqrt(term_sqrt) * math.cos(inc_rad)


def cr3bp_jacobi_constant(
    x: float, y: float, z: float,
    vx: float, vy: float, vz: float,
    mu_cr3bp: float
) -> float:
    """
    Calculates the Jacobi energy integral in the nondimensional CR3BP frame:
    C_J = 2 * Omega(x, y, z) - (vx^2 + vy^2 + vz^2)
    where Omega(x, y, z) = 0.5 * (x^2 + y^2) + (1 - mu)/r1 + mu/r2
    """
    if not (0.0 < mu_cr3bp < 0.5):
        raise ValueError(f"CR3BP mass ratio mu must be in (0, 0.5), got {mu_cr3bp}")
    
    r1 = math.sqrt((x + mu_cr3bp) ** 2 + y * y + z * z)
    r2 = math.sqrt((x - 1.0 + mu_cr3bp) ** 2 + y * y + z * z)
    
    if r1 < 1e-9 or r2 < 1e-9:
        raise ValueError("Singularity: position collides with primary or secondary body.")
    
    omega = 0.5 * (x * x + y * y) + ((1.0 - mu_cr3bp) / r1) + (mu_cr3bp / r2)
    v_sq = vx * vx + vy * vy + vz * vz
    return 2.0 * omega - v_sq


def srp_acceleration(
    flux_p0: float,
    r_au: float,
    area_m2: float,
    mass_kg: float,
    reflectivity_rho: float,
    sun_angle_rad: float
) -> float:
    """
    Computes solar radiation pressure non-gravitational acceleration:
    a_srp = P0 * (1/r_au^2) * (A / m) * (1 + rho) * cos(theta) (m/s^2)
    """
    if r_au <= 0:
        raise ValueError("Distance in AU must be positive.")
    if mass_kg <= 0 or area_m2 <= 0:
        raise ValueError("Mass and area must be positive.")
    if not (0.0 <= reflectivity_rho <= 1.0):
        raise ValueError(f"Reflectivity rho must be in [0, 1], got {reflectivity_rho}")
    
    flux_at_r = flux_p0 / (r_au * r_au)
    return flux_at_r * (area_m2 / mass_kg) * (1.0 + reflectivity_rho) * math.cos(sun_angle_rad)


def validate_interplanetary_mission(
    nominal_delta_v_km_s: float,
    propellant_budget_delta_v_km_s: float,
    tisserand_pre: float,
    tisserand_post: float,
    periapsis_altitude_km: float,
    min_safe_altitude_km: float,
    jacobi_c: float,
    min_jacobi_barrier: float,
    srp_unmodeled_accel_m_s2: float,
    max_allowed_srp_drift: float = 1.0e-6
) -> TrajectoryValidationResult:
    """
    Performs comprehensive verification of an interplanetary trajectory against
    all astrodynamic and celestial mechanics invariants.
    """
    violations = []
    
    # 1. Delta-v margin safety factor
    if nominal_delta_v_km_s <= 0:
        propellant_margin_sf = 0.0
        violations.append("Nominal delta-v must be strictly positive.")
    else:
        propellant_margin_sf = propellant_budget_delta_v_km_s / nominal_delta_v_km_s
        if propellant_margin_sf < 1.15:
            violations.append(
                f"Propellant delta-v margin safety factor {propellant_margin_sf:.3f} < 1.15 minimum reserve."
            )
            
    # 2. Tisserand parameter invariance
    tiss_diff = abs(tisserand_post - tisserand_pre)
    if tiss_diff > 0.05:
        violations.append(
            f"Tisserand parameter jump |Delta T_p| = {tiss_diff:.4f} > 0.05 limit across flyby."
        )
        
    # 3. Flyby periapsis altitude clearance
    if periapsis_altitude_km < min_safe_altitude_km:
        violations.append(
            f"Flyby periapsis altitude {periapsis_altitude_km:.1f} km < {min_safe_altitude_km:.1f} km safe boundary."
        )
        
    # 4. Jacobi constant energy barrier
    if jacobi_c < min_jacobi_barrier:
        violations.append(
            f"Jacobi constant {jacobi_c:.4f} < {min_jacobi_barrier:.4f} barrier; manifold escape risk."
        )
        
    # 5. Non-gravitational SRP drift
    if srp_unmodeled_accel_m_s2 > max_allowed_srp_drift:
        violations.append(
            f"Unmodeled SRP drift {srp_unmodeled_accel_m_s2:.2e} m/s^2 > {max_allowed_srp_drift:.2e} m/s^2 limit."
        )
        
    is_valid = (len(violations) == 0)
    return TrajectoryValidationResult(
        is_valid=is_valid,
        delta_v_total=nominal_delta_v_km_s,
        propellant_margin_sf=propellant_margin_sf,
        tisserand_error=tiss_diff,
        periapsis_clearance_km=periapsis_altitude_km,
        jacobi_constant=jacobi_c,
        srp_drift_accel=srp_unmodeled_accel_m_s2,
        violations=violations
    )
