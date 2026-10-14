#!/usr/bin/env python3
"""
Direct Fusion Rocket & Magnetoplasmadynamic Propulsion References
Domain Invariants: Ultra-high specific impulse, magnetic nozzle Alfven detachment Mach number,
Pennes bioheat equivalent HTS neutron shielding, nozzle cosine divergence efficiency,
and plasma thrust-to-power conversion.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List

STANDARD_GRAVITY = 9.80665  # m / s^2
VACUUM_PERMEABILITY = 1.25663706212e-6  # H / m


@dataclass
class FusionRocketValidationResult:
    is_valid: bool
    specific_impulse_s: float
    alfven_mach: float
    divergence_half_angle_deg: float
    neutron_wall_flux_mw_m2: float
    thrust_efficiency_pct: float
    plasma_purity_pct: float
    violations: List[str] = field(default_factory=list)


def exhaust_velocity_from_isp(isp_s: float) -> float:
    """
    Computes effective exhaust velocity:
    v_e = I_sp * g_0
    """
    if isp_s <= 0:
        raise ValueError("Specific impulse must be strictly positive.")
    return isp_s * STANDARD_GRAVITY


def alfven_velocity(b_field_t: float, mass_density_kg_m3: float) -> float:
    """
    Computes Alfven wave propagation velocity in magnetized plasma:
    v_A = B / sqrt(mu_0 * rho)
    """
    if b_field_t <= 0 or mass_density_kg_m3 <= 0:
        raise ValueError("Magnetic field and plasma mass density must be positive.")
    return b_field_t / math.sqrt(VACUUM_PERMEABILITY * mass_density_kg_m3)


def magnetic_nozzle_alfven_mach(
    v_exhaust_m_s: float,
    b_field_t: float,
    mass_density_kg_m3: float
) -> float:
    """
    Computes Alfven Mach number M_A = v_exhaust / v_Alfven for magnetic nozzle plasma detachment:
    Clean detachment requires M_A >= 1.50 (kinetic energy exceeds magnetic field tension).
    """
    if v_exhaust_m_s <= 0:
        raise ValueError("Exhaust velocity must be strictly positive.")
    v_a = alfven_velocity(b_field_t, mass_density_kg_m3)
    return v_exhaust_m_s / v_a


def nozzle_divergence_efficiency(half_angle_deg: float) -> float:
    """
    Calculates cosine divergence thrust efficiency:
    eta_div = (1 + cos(theta)) / 2
    """
    if not (0.0 <= half_angle_deg <= 90.0):
        raise ValueError("Nozzle divergence half-angle must be between 0 and 90 degrees.")
    rad = math.radians(half_angle_deg)
    return (1.0 + math.cos(rad)) / 2.0


def thrust_power_efficiency(thrust_n: float, mass_flow_kg_s: float, fusion_power_w: float) -> float:
    """
    Computes kinetic thrust efficiency:
    eta_thrust = (F^2 / (2 * m_dot * P_fusion)) * 100%
    """
    if thrust_n <= 0 or mass_flow_kg_s <= 0 or fusion_power_w <= 0:
        raise ValueError("Thrust, mass flow, and fusion power must be strictly positive.")
    p_jet = (thrust_n ** 2) / (2.0 * mass_flow_kg_s)
    return (p_jet / fusion_power_w) * 100.0


def validate_fusion_rocket(
    specific_impulse_s: float,
    alfven_mach: float,
    divergence_half_angle_deg: float,
    neutron_wall_flux_mw_m2: float,
    thrust_efficiency_pct: float,
    plasma_purity_pct: float
) -> FusionRocketValidationResult:
    """
    Validates a direct fusion rocket engine against plasma detachment,
    thermal coil shielding, and specific impulse invariants.
    """
    violations = []

    # 1. Specific Impulse (>= 10,000 s)
    if specific_impulse_s < 10000.0:
        violations.append(
            f"Specific impulse {specific_impulse_s:.0f} s < 10,000 s minimum; fails fusion-class exhaust velocity benchmark."
        )

    # 2. Magnetic Nozzle Detachment Alfven Mach (>= 1.50)
    if alfven_mach < 1.50:
        violations.append(
            f"Alfven Mach number M_A={alfven_mach:.2f} < 1.50 limit; plasma trapped on closed field lines producing zero net thrust."
        )

    # 3. Nozzle Divergence Half-Angle (<= 12.0 deg)
    if divergence_half_angle_deg > 12.0:
        violations.append(
            f"Divergence half-angle {divergence_half_angle_deg:.1f} deg > 12.0 deg threshold; excessive cosine thrust momentum loss."
        )

    # 4. Neutron Wall Heat Flux (<= 2.0 MW/m^2)
    if neutron_wall_flux_mw_m2 > 2.0:
        violations.append(
            f"Neutron wall flux {neutron_wall_flux_mw_m2:.2f} MW/m^2 > 2.0 MW/m^2 limit; causes HTS magnetic coil thermal quench."
        )

    # 5. Thrust Power Efficiency (>= 65.0%)
    if thrust_efficiency_pct < 65.0:
        violations.append(
            f"Thrust efficiency {thrust_efficiency_pct:.1f}% < 65.0% threshold; excessive parasitic thermal recirculation."
        )

    # 6. Plasma Exhaust Jet Purity (>= 98.0%)
    if plasma_purity_pct < 98.0:
        violations.append(
            f"Plasma ionization purity {plasma_purity_pct:.1f}% < 98.0% threshold; unionized neutral boundary drag."
        )

    is_valid = (len(violations) == 0)
    return FusionRocketValidationResult(
        is_valid=is_valid,
        specific_impulse_s=specific_impulse_s,
        alfven_mach=alfven_mach,
        divergence_half_angle_deg=divergence_half_angle_deg,
        neutron_wall_flux_mw_m2=neutron_wall_flux_mw_m2,
        thrust_efficiency_pct=thrust_efficiency_pct,
        plasma_purity_pct=plasma_purity_pct,
        violations=violations
    )
