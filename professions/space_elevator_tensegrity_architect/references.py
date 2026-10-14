"""Physical references and mathematical models for Space Elevator & Active Tensegrity Megastructures.

Architect: Dr. Valerius 'The Megastructure' Sterling
Domain: space_elevator_tensegrity_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Planetary and physical constants
GRAVITATIONAL_CONSTANT: float = 6.67430e-11   # m^3 / (kg * s^2)
EARTH_MASS_KG: float = 5.9722e24             # kg
EARTH_EQUATORIAL_RADIUS_M: float = 6.378137e6 # m (6,378.137 km)
EARTH_ANGULAR_VELOCITY_RAD_S: float = 7.2921159e-5  # rad/s

# Standard geostationary orbit radius: r_GEO = (G * M_E / omega^2)^(1/3)
GEOSTATIONARY_RADIUS_M: float = (
    (GRAVITATIONAL_CONSTANT * EARTH_MASS_KG) / (EARTH_ANGULAR_VELOCITY_RAD_S ** 2)
) ** (1.0 / 3.0)  # ~4.2164e7 m (42,164 km)
GEOSTATIONARY_ALTITUDE_M: float = GEOSTATIONARY_RADIUS_M - EARTH_EQUATORIAL_RADIUS_M  # ~3.5786e7 m (35,786 km)

# Standard engineering bounds for carbon-nanotube / graphene tensegrity ribbon
MIN_TENSILE_STRENGTH_PA: float = 6.5e10       # 65.0 GPa
MAX_TETHER_DENSITY_KG_M3: float = 1300.0      # 1300.0 kg/m^3
MIN_SPECIFIC_STRENGTH_N_M_KG: float = 5.0e7   # 50.0 MYuri (5.0e7 N*m/kg)
MAX_TAPER_RATIO: float = 2.50                 # Area(GEO) / Area(Anchor) <= 2.50
MIN_TETHER_LENGTH_M: float = 1.0e8            # 100,000 km
MIN_ANCHOR_PRETENSION_N: float = 1.0e7        # 10.0 MN
MAX_CLIMBER_MASS_KG: float = 20000.0          # 20 metric tons
MAX_CLIMBER_VELOCITY_M_S: float = 55.56       # 200.0 km/h (~55.56 m/s)
MAX_CORIOLIS_DEFLECTION_RAD: float = 0.05     # 0.05 rad (2.86 deg)
MIN_ACTIVE_DAMPING_RATIO: float = 0.05        # 5.0% of critical damping
MAX_RESONANT_QUALITY_FACTOR: float = 20.0     # Q <= 20.0
MIN_WAVE_VELOCITY_M_S: float = 7000.0         # 7000.0 m/s


def calculate_specific_strength(
    tensile_strength_pa: float,
    density_kg_m3: float
) -> float:
    """Calculate material specific strength in N*m/kg (Yuri)."""
    if density_kg_m3 <= 0.0 or tensile_strength_pa <= 0.0:
        return 0.0
    return tensile_strength_pa / density_kg_m3


def calculate_tether_taper_ratio(
    tensile_strength_pa: float,
    density_kg_m3: float
) -> float:
    """Calculate exponential cross-sectional area taper ratio from Earth surface to GEO.

    lambda = exp( (rho / sigma_t) * Delta_Phi )
    """
    if tensile_strength_pa <= 0.0 or density_kg_m3 <= 0.0:
        return float("inf")

    gm = GRAVITATIONAL_CONSTANT * EARTH_MASS_KG
    r0 = EARTH_EQUATORIAL_RADIUS_M
    r_geo = GEOSTATIONARY_RADIUS_M
    omega = EARTH_ANGULAR_VELOCITY_RAD_S

    # Gravitational potential difference: GM/r0 - GM/r_geo
    delta_grav = (gm / r0) - (gm / r_geo)
    # Centrifugal potential difference: 0.5 * omega^2 * (r_geo^2 - r0^2)
    delta_centrif = 0.5 * (omega ** 2) * ((r_geo ** 2) - (r0 ** 2))
    delta_phi = delta_grav - delta_centrif

    exponent = (density_kg_m3 * delta_phi) / tensile_strength_pa
    if exponent > 700:
        return float("inf")
    return math.exp(exponent)


def calculate_coriolis_deflection(
    climber_mass_kg: float,
    climber_velocity_m_s: float,
    effective_gravity_m_s2: float = 9.81
) -> Tuple[float, float]:
    """Calculate Coriolis lateral drag force and equilibrium tether deflection angle.

    F_c = 2 * M * omega * v
    theta = F_c / (M * g_eff) = 2 * omega * v / g_eff
    """
    if climber_mass_kg <= 0.0 or climber_velocity_m_s <= 0.0 or effective_gravity_m_s2 <= 0.0:
        return 0.0, 0.0

    omega = EARTH_ANGULAR_VELOCITY_RAD_S
    f_coriolis = 2.0 * climber_mass_kg * omega * climber_velocity_m_s
    theta_rad = (2.0 * omega * climber_velocity_m_s) / effective_gravity_m_s2
    return f_coriolis, theta_rad


def calculate_transverse_wave_speed(
    tension_n: float,
    linear_density_kg_m: float
) -> float:
    """Calculate transverse acoustic wave velocity along tensegrity tether."""
    if tension_n <= 0.0 or linear_density_kg_m <= 0.0:
        return 0.0
    return math.sqrt(tension_n / linear_density_kg_m)


@dataclass
class SpaceElevatorValidationResult:
    """Structured validation report for Space Elevator & Tensegrity Megastructures."""
    is_valid: bool
    tensile_strength_gpa: float
    tether_density_kg_m3: float
    specific_strength_myuri: float
    taper_ratio: float
    tether_length_km: float
    anchor_pretension_mn: float
    climber_mass_kg: float
    climber_velocity_km_h: float
    coriolis_deflection_rad: float
    active_damping_ratio: float
    quality_factor: float
    wave_velocity_m_s: float
    flaws: List[str]


def validate_space_elevator_parameters(
    tensile_strength_gpa: float = 85.0,
    tether_density_kg_m3: float = 1250.0,
    tether_length_km: float = 105000.0,
    anchor_pretension_mn: float = 14.5,
    climber_mass_kg: float = 15000.0,
    climber_velocity_km_h: float = 180.0,
    active_damping_ratio: float = 0.08,
    quality_factor: float = 12.5,
    wave_velocity_m_s: float = 9200.0
) -> SpaceElevatorValidationResult:
    """Validate space elevator engineering parameters against Dr. Valerius Sterling's strict megastructure benchmarks."""
    flaws: List[str] = []

    tensile_pa = tensile_strength_gpa * 1e9
    if tensile_pa < MIN_TENSILE_STRENGTH_PA:
        flaws.append(
            f"Tensile strength {tensile_strength_gpa:.1f} GPa below minimum allowable {MIN_TENSILE_STRENGTH_PA / 1e9:.1f} GPa."
        )

    if tether_density_kg_m3 > MAX_TETHER_DENSITY_KG_M3:
        flaws.append(
            f"Tether material density {tether_density_kg_m3:.1f} kg/m^3 exceeds ceiling {MAX_TETHER_DENSITY_KG_M3:.1f} kg/m^3."
        )

    spec_strength = calculate_specific_strength(tensile_pa, tether_density_kg_m3)
    spec_strength_myuri = spec_strength / 1e6
    if spec_strength < MIN_SPECIFIC_STRENGTH_N_M_KG:
        flaws.append(
            f"Specific strength {spec_strength_myuri:.1f} MYuri below threshold {MIN_SPECIFIC_STRENGTH_N_M_KG / 1e6:.1f} MYuri."
        )

    taper = calculate_tether_taper_ratio(tensile_pa, tether_density_kg_m3)
    if taper > MAX_TAPER_RATIO:
        flaws.append(
            f"Geostationary taper ratio {taper:.2f} exceeds exponential mass ceiling {MAX_TAPER_RATIO:.2f}."
        )

    tether_len_m = tether_length_km * 1000.0
    if tether_len_m < MIN_TETHER_LENGTH_M:
        flaws.append(
            f"Total tether length {tether_length_km:.0f} km below orbital equilibrium requirement {MIN_TETHER_LENGTH_M / 1000.0:.0f} km."
        )

    anchor_pretension_n = anchor_pretension_mn * 1e6
    if anchor_pretension_n < MIN_ANCHOR_PRETENSION_N:
        flaws.append(
            f"Anchor pretension {anchor_pretension_mn:.1f} MN below upward tension threshold {MIN_ANCHOR_PRETENSION_N / 1e6:.1f} MN."
        )

    if climber_mass_kg > MAX_CLIMBER_MASS_KG:
        flaws.append(
            f"Payload climber mass {climber_mass_kg:.0f} kg exceeds dynamic load envelope {MAX_CLIMBER_MASS_KG:.0f} kg."
        )

    climber_v_m_s = climber_velocity_km_h / 3.6
    if climber_v_m_s > MAX_CLIMBER_VELOCITY_M_S:
        flaws.append(
            f"Climber transit velocity {climber_velocity_km_h:.1f} km/h ({climber_v_m_s:.1f} m/s) exceeds maximum {MAX_CLIMBER_VELOCITY_M_S * 3.6:.1f} km/h."
        )

    _, theta_coriolis = calculate_coriolis_deflection(climber_mass_kg, climber_v_m_s)
    if theta_coriolis > MAX_CORIOLIS_DEFLECTION_RAD:
        flaws.append(
            f"Coriolis lateral deflection angle {theta_coriolis:.4f} rad exceeds stability limit {MAX_CORIOLIS_DEFLECTION_RAD:.4f} rad."
        )

    if active_damping_ratio < MIN_ACTIVE_DAMPING_RATIO:
        flaws.append(
            f"Active transverse damping ratio {active_damping_ratio:.3f} below minimum {MIN_ACTIVE_DAMPING_RATIO:.3f} (5.0%)."
        )

    if quality_factor > MAX_RESONANT_QUALITY_FACTOR:
        flaws.append(
            f"Resonant quality factor Q={quality_factor:.1f} exceeds harmonic safety bound Q={MAX_RESONANT_QUALITY_FACTOR:.1f}."
        )

    if wave_velocity_m_s < MIN_WAVE_VELOCITY_M_S:
        flaws.append(
            f"Transverse wave velocity {wave_velocity_m_s:.1f} m/s below stiffness threshold {MIN_WAVE_VELOCITY_M_S:.1f} m/s."
        )

    return SpaceElevatorValidationResult(
        is_valid=len(flaws) == 0,
        tensile_strength_gpa=tensile_strength_gpa,
        tether_density_kg_m3=tether_density_kg_m3,
        specific_strength_myuri=spec_strength_myuri,
        taper_ratio=taper,
        tether_length_km=tether_length_km,
        anchor_pretension_mn=anchor_pretension_mn,
        climber_mass_kg=climber_mass_kg,
        climber_velocity_km_h=climber_velocity_km_h,
        coriolis_deflection_rad=theta_coriolis,
        active_damping_ratio=active_damping_ratio,
        quality_factor=quality_factor,
        wave_velocity_m_s=wave_velocity_m_s,
        flaws=flaws
    )
