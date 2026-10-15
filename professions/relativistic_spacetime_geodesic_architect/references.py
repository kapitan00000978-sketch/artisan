"""Physical references and mathematical models for Relativistic Spacetime Geodesics & Black Hole Magnetospheres.

Architect: Dr. Veda 'The Spacetime' Vance
Domain: relativistic_spacetime_geodesic_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Fundamental physical constants
SPEED_OF_LIGHT: float = 299792458.0                # m/s
GRAVITATIONAL_CONSTANT: float = 6.67430e-11        # m^3/(kg*s^2)
SOLAR_MASS_KG: float = 1.98847e30                  # kg
VACUUM_PERMEABILITY: float = 4.0 * math.pi * 1.0e-7 # H/m

# Quantitative engineering benchmarks for Kerr black hole spacetime numerical integration
MAX_KERR_SPIN_PARAMETER: float = 0.998             # Thorne accretion equilibrium bound |a_*| <= 0.998
MAX_SYMPLECTIC_ENERGY_DRIFT: float = 1.0e-10       # |Delta E / E_0| <= 1.0e-10
MAX_ANGULAR_MOMENTUM_DRIFT: float = 1.0e-10        # |Delta L_z / L_z0| <= 1.0e-10
MAX_CARTER_CONSTANT_DRIFT: float = 1.0e-10         # |Delta Q / Q_0| <= 1.0e-10
MIN_BZ_JET_POWER_W: float = 1.0e38                 # P_BZ >= 1.0e38 Watts
MIN_INTEGRATOR_ORDER: int = 4                      # Minimum 4th-order symplectic scheme (e.g. Yoshida / Gauss-Legendre)
SCHWARZSCHILD_CRITICAL_IMPACT: float = math.sqrt(27.0)  # b_c = sqrt(27) * M ~= 5.19615 M


def calculate_kerr_horizons(mass_m: float, spin_a: float) -> Tuple[float, float]:
    """Calculate the event horizon r_+ and Cauchy horizon r_- for a Kerr black hole.

    r_+- = M +- sqrt(M^2 - a^2)
    """
    if mass_m <= 0.0 or abs(spin_a) > mass_m:
        return 0.0, 0.0
    disc = math.sqrt(max(0.0, (mass_m ** 2) - (spin_a ** 2)))
    r_plus = mass_m + disc
    r_minus = mass_m - disc
    return r_plus, r_minus


def calculate_kerr_ergosphere_radius(mass_m: float, spin_a: float, theta_rad: float) -> float:
    """Calculate the static limit ergosurface radius at polar angle theta.

    r_ergo(theta) = M + sqrt(M^2 - a^2 * cos^2(theta))
    """
    if mass_m <= 0.0:
        return 0.0
    cos_theta = math.cos(theta_rad)
    disc = math.sqrt(max(0.0, (mass_m ** 2) - ((spin_a ** 2) * (cos_theta ** 2))))
    return mass_m + disc


def calculate_isco_radius(
    mass_m: float,
    dimensionless_spin: float,
    prograde: bool = True
) -> float:
    """Calculate the Innermost Stable Circular Orbit (ISCO) radius in geometric units.

    r_ISCO = M * (3 + Z2 -+ sqrt((3 - Z1) * (3 + Z1 + 2 * Z2)))
    """
    if mass_m <= 0.0:
        return 0.0
    a_star = max(-0.998, min(0.998, dimensionless_spin))

    z1 = 1.0 + ((1.0 - (a_star ** 2)) ** (1.0 / 3.0)) * (
        ((1.0 + a_star) ** (1.0 / 3.0)) + ((1.0 - a_star) ** (1.0 / 3.0))
    )
    z2 = math.sqrt((3.0 * (a_star ** 2)) + (z1 ** 2))

    sign = -1.0 if prograde else 1.0
    term = max(0.0, (3.0 - z1) * (3.0 + z1 + (2.0 * z2)))
    return mass_m * (3.0 + z2 + (sign * math.sqrt(term)))


def calculate_blandford_znajek_power(
    mass_kg: float,
    dimensionless_spin: float,
    magnetic_flux_weber: float
) -> float:
    """Calculate Blandford-Znajek jet extraction power in Watts.

    P_BZ = (k / 4pi*c) * (Omega_H * r_H / c)^2 * Phi_BH^2
    """
    if mass_kg <= 0.0 or magnetic_flux_weber <= 0.0:
        return 0.0

    # Geometric scale: r_g = G*M / c^2
    r_g = (GRAVITATIONAL_CONSTANT * mass_kg) / (SPEED_OF_LIGHT ** 2)
    a_star = max(-0.998, min(0.998, dimensionless_spin))

    # Horizon radius in meters
    r_h = r_g * (1.0 + math.sqrt(max(0.0, 1.0 - (a_star ** 2))))

    # Angular frequency of horizon Omega_H in rad/s
    omega_h = (a_star * SPEED_OF_LIGHT) / (2.0 * r_h)

    # Dimensionless factor k ~ 0.053 for split monopole
    k_factor = 0.053
    efficiency = ((omega_h * r_h) / SPEED_OF_LIGHT) ** 2
    return (k_factor / (4.0 * math.pi * SPEED_OF_LIGHT * VACUUM_PERMEABILITY)) * efficiency * (magnetic_flux_weber ** 2)


@dataclass
class SpacetimeGeodesicValidationResult:
    """Structured validation report for Relativistic Spacetime Geodesics & Black Hole Physics."""
    is_valid: bool
    dimensionless_spin: float
    symplectic_energy_drift: float
    angular_momentum_drift: float
    carter_constant_drift: float
    bz_jet_power_w: float
    integrator_order: int
    isco_radius_m: float
    outer_horizon_radius_m: float
    flaws: List[str]


def validate_spacetime_geodesic_parameters(
    dimensionless_spin: float = 0.94,
    symplectic_energy_drift: float = 4.2e-12,
    angular_momentum_drift: float = 3.8e-12,
    carter_constant_drift: float = 5.1e-12,
    bz_jet_power_w: float = 4.5e38,
    integrator_order: int = 4,
    isco_radius_m: float = 2.05,
    outer_horizon_radius_m: float = 1.34
) -> SpacetimeGeodesicValidationResult:
    """Validate relativistic spacetime parameters against Dr. Veda Vance's strict benchmarks."""
    flaws: List[str] = []

    if abs(dimensionless_spin) > MAX_KERR_SPIN_PARAMETER:
        flaws.append(
            f"Kerr spin parameter |a_*| {abs(dimensionless_spin):.4f} exceeds Thorne equilibrium limit "
            f"{MAX_KERR_SPIN_PARAMETER:.3f} (violating cosmic censorship boundary)."
        )

    if symplectic_energy_drift > MAX_SYMPLECTIC_ENERGY_DRIFT:
        flaws.append(
            f"Symplectic energy invariant drift {symplectic_energy_drift:.2e} exceeds precision ceiling "
            f"{MAX_SYMPLECTIC_ENERGY_DRIFT:.2e}."
        )

    if angular_momentum_drift > MAX_ANGULAR_MOMENTUM_DRIFT:
        flaws.append(
            f"Axial angular momentum drift {angular_momentum_drift:.2e} exceeds symplectic ceiling "
            f"{MAX_ANGULAR_MOMENTUM_DRIFT:.2e}."
        )

    if carter_constant_drift > MAX_CARTER_CONSTANT_DRIFT:
        flaws.append(
            f"Carter constant invariant drift {carter_constant_drift:.2e} exceeds symplectic limit "
            f"{MAX_CARTER_CONSTANT_DRIFT:.2e}."
        )

    if bz_jet_power_w < MIN_BZ_JET_POWER_W:
        flaws.append(
            f"Blandford-Znajek magnetospheric jet power {bz_jet_power_w:.2e} W below extraction benchmark "
            f"{MIN_BZ_JET_POWER_W:.2e} W."
        )

    if integrator_order < MIN_INTEGRATOR_ORDER:
        flaws.append(
            f"Geodesic integrator order {integrator_order} below minimum required symplectic order {MIN_INTEGRATOR_ORDER}."
        )

    if isco_radius_m < 1.0 or isco_radius_m > 9.0:
        flaws.append(
            f"ISCO radius {isco_radius_m:.3f} M outside Kerr physical bounds [1.0 M, 9.0 M]."
        )

    if outer_horizon_radius_m < 1.0 or outer_horizon_radius_m > 2.0:
        flaws.append(
            f"Outer event horizon radius {outer_horizon_radius_m:.3f} M outside Kerr physical bounds [1.0 M, 2.0 M]."
        )

    return SpacetimeGeodesicValidationResult(
        is_valid=len(flaws) == 0,
        dimensionless_spin=dimensionless_spin,
        symplectic_energy_drift=symplectic_energy_drift,
        angular_momentum_drift=angular_momentum_drift,
        carter_constant_drift=carter_constant_drift,
        bz_jet_power_w=bz_jet_power_w,
        integrator_order=integrator_order,
        isco_radius_m=isco_radius_m,
        outer_horizon_radius_m=outer_horizon_radius_m,
        flaws=flaws
    )
