"""Physical references and mathematical models for Interstellar Bussard Ramjets & Magnetic Scoops.

Architect: Dr. Zephyrus 'The Void' Vance
Domain: interstellar_ramjet_bussard_propulsion_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Fundamental physical constants
SPEED_OF_LIGHT: float = 299792458.0                 # m/s
PROTON_MASS_KG: float = 1.67262192369e-27           # kg
ELEMENTARY_CHARGE: float = 1.602176634e-19          # C
VACUUM_PERMITTIVITY: float = 8.8541878128e-12       # F/m

# Quantitative engineering benchmarks for Interstellar Bussard Ramjets
MIN_SCOOP_RADIUS_KM: float = 1000.0                 # R_scoop >= 1000.0 km
MIN_RELATIVISTIC_VELOCITY_FRACTION: float = 0.10     # beta >= 0.10 (v >= 0.10 c)
MIN_MAGNETIC_SCOOP_FIELD_T: float = 15.0            # B_scoop >= 15.0 T
MIN_PHOTO_IONIZATION_EFFICIENCY: float = 0.98        # eta_ion >= 0.98 (98%)
MIN_CAPTURE_CROSS_SECTION_EFFICIENCY: float = 0.85  # eta_capture >= 0.85 (85%)
MIN_THRUST_TO_DRAG_RATIO: float = 1.25              # F_thrust / F_drag >= 1.25
MIN_EXHAUST_VELOCITY_M_S: float = 3.0e7             # v_e >= 3.0e7 m/s (0.10 c)
MIN_NOZZLE_COLLIMATION_EFFICIENCY: float = 0.88     # eta_collimation >= 0.88 (88%)
MIN_SHIP_ACCELERATION_M_S2: float = 0.98            # a_ship >= 0.98 m/s^2 (0.10 g)
MAX_SHIP_ACCELERATION_M_S2: float = 9.81            # a_ship <= 9.81 m/s^2 (1.00 g)
MIN_CORE_FUSION_TEMP_K: float = 1.0e8               # T_core >= 1.0e8 K (100 MK)
MAX_BREMSSTRAHLUNG_LOSS_RATIO: float = 0.40         # P_brem / P_fusion <= 0.40


def calculate_lorentz_factor(velocity_fraction_beta: float) -> float:
    """Calculate relativistic Lorentz factor gamma from beta = v/c.

    gamma = 1 / sqrt(1 - beta^2)
    """
    if velocity_fraction_beta < 0.0 or velocity_fraction_beta >= 1.0:
        return 1.0
    return 1.0 / math.sqrt(max(1e-15, 1.0 - (velocity_fraction_beta ** 2)))


def calculate_proton_intake_rate(
    scoop_radius_m: float,
    velocity_m_s: float,
    ism_density_m3: float = 1.0e6,
    capture_eff: float = 0.85
) -> float:
    """Calculate proton intake mass flow rate in kg/s.

    mdot = pi * R_scoop^2 * v * n_ISM * m_p * eta_capture
    """
    if scoop_radius_m <= 0.0 or velocity_m_s <= 0.0 or ism_density_m3 <= 0.0 or capture_eff <= 0.0:
        return 0.0

    area = math.pi * (scoop_radius_m ** 2)
    mass_density = ism_density_m3 * PROTON_MASS_KG
    return area * velocity_m_s * mass_density * capture_eff


def calculate_relativistic_ram_drag(
    scoop_radius_m: float,
    velocity_m_s: float,
    ism_density_m3: float = 1.0e6
) -> float:
    """Calculate relativistic interstellar ram-drag in Newtons.

    F_drag = 2 * pi * R_scoop^2 * n_ISM * m_p * v^2 * gamma
    """
    if scoop_radius_m <= 0.0 or velocity_m_s <= 0.0 or ism_density_m3 <= 0.0:
        return 0.0

    beta = min(0.9999, velocity_m_s / SPEED_OF_LIGHT)
    gamma = calculate_lorentz_factor(beta)
    area = math.pi * (scoop_radius_m ** 2)
    mass_density = ism_density_m3 * PROTON_MASS_KG
    return 2.0 * area * mass_density * (velocity_m_s ** 2) * gamma


def calculate_fusion_thrust(
    mass_flow_rate_kg_s: float,
    exhaust_velocity_m_s: float,
    collimation_eff: float = 0.88
) -> float:
    """Calculate thermonuclear fusion thrust in Newtons.

    F_thrust = mdot * v_e * eta_collimation
    """
    if mass_flow_rate_kg_s <= 0.0 or exhaust_velocity_m_s <= 0.0 or collimation_eff <= 0.0:
        return 0.0
    return mass_flow_rate_kg_s * exhaust_velocity_m_s * collimation_eff


@dataclass
class BussardRamjetValidationResult:
    """Structured validation report for Interstellar Bussard Ramjet parameters."""
    is_valid: bool
    scoop_radius_km: float
    flight_velocity_beta: float
    magnetic_scoop_field_t: float
    photo_ionization_efficiency: float
    capture_cross_section_efficiency: float
    thrust_to_drag_ratio: float
    exhaust_velocity_m_s: float
    nozzle_collimation_efficiency: float
    ship_acceleration_m_s2: float
    core_fusion_temp_k: float
    bremsstrahlung_loss_ratio: float
    flaws: List[str]


def validate_bussard_ramjet_parameters(
    scoop_radius_km: float = 1200.0,
    flight_velocity_beta: float = 0.25,
    magnetic_scoop_field_t: float = 18.5,
    photo_ionization_efficiency: float = 0.992,
    capture_cross_section_efficiency: float = 0.89,
    thrust_to_drag_ratio: float = 1.45,
    exhaust_velocity_m_s: float = 4.2e7,
    nozzle_collimation_efficiency: float = 0.92,
    ship_acceleration_m_s2: float = 4.5,
    core_fusion_temp_k: float = 1.5e8,
    bremsstrahlung_loss_ratio: float = 0.28
) -> BussardRamjetValidationResult:
    """Validate interstellar ramjet parameters against Dr. Zephyrus Vance's strict benchmarks."""
    flaws: List[str] = []

    if scoop_radius_km < MIN_SCOOP_RADIUS_KM:
        flaws.append(
            f"Magnetic scoop radius {scoop_radius_km:.1f} km below minimum interstellar intake benchmark "
            f"{MIN_SCOOP_RADIUS_KM:.1f} km."
        )

    if flight_velocity_beta < MIN_RELATIVISTIC_VELOCITY_FRACTION:
        flaws.append(
            f"Interstellar cruise velocity fraction beta {flight_velocity_beta:.3f} below minimum relativistic floor "
            f"{MIN_RELATIVISTIC_VELOCITY_FRACTION:.2f}."
        )

    if magnetic_scoop_field_t < MIN_MAGNETIC_SCOOP_FIELD_T:
        flaws.append(
            f"Magnetic scoop on-axis choke field {magnetic_scoop_field_t:.1f} T below required confinement field "
            f"{MIN_MAGNETIC_SCOOP_FIELD_T:.1f} T."
        )

    if photo_ionization_efficiency < MIN_PHOTO_IONIZATION_EFFICIENCY:
        flaws.append(
            f"Forward photo-ionization efficiency {photo_ionization_efficiency:.3f} below ionization floor "
            f"{MIN_PHOTO_IONIZATION_EFFICIENCY:.2f} (neutral gas blowby risk)."
        )

    if capture_cross_section_efficiency < MIN_CAPTURE_CROSS_SECTION_EFFICIENCY:
        flaws.append(
            f"Proton capture cross-section efficiency {capture_cross_section_efficiency:.3f} below benchmark "
            f"{MIN_CAPTURE_CROSS_SECTION_EFFICIENCY:.2f}."
        )

    if thrust_to_drag_ratio < MIN_THRUST_TO_DRAG_RATIO:
        flaws.append(
            f"Thrust-to-drag ratio {thrust_to_drag_ratio:.2f} below net-acceleration floor "
            f"{MIN_THRUST_TO_DRAG_RATIO:.2f} (deceleration drag catastrophe)."
        )

    if exhaust_velocity_m_s < MIN_EXHAUST_VELOCITY_M_S:
        flaws.append(
            f"Thermonuclear exhaust velocity {exhaust_velocity_m_s:.2e} m/s below relativistic benchmark "
            f"{MIN_EXHAUST_VELOCITY_M_S:.2e} m/s."
        )

    if nozzle_collimation_efficiency < MIN_NOZZLE_COLLIMATION_EFFICIENCY:
        flaws.append(
            f"Magnetic nozzle collimation efficiency {nozzle_collimation_efficiency:.3f} below minimum "
            f"{MIN_NOZZLE_COLLIMATION_EFFICIENCY:.2f}."
        )

    if ship_acceleration_m_s2 < MIN_SHIP_ACCELERATION_M_S2 or ship_acceleration_m_s2 > MAX_SHIP_ACCELERATION_M_S2:
        flaws.append(
            f"Ship continuous acceleration {ship_acceleration_m_s2:.2f} m/s^2 outside operational envelope "
            f"[{MIN_SHIP_ACCELERATION_M_S2:.2f}, {MAX_SHIP_ACCELERATION_M_S2:.2f}] m/s^2."
        )

    if core_fusion_temp_k < MIN_CORE_FUSION_TEMP_K:
        flaws.append(
            f"Core thermonuclear reaction temperature {core_fusion_temp_k:.2e} K below fusion threshold "
            f"{MIN_CORE_FUSION_TEMP_K:.2e} K."
        )

    if bremsstrahlung_loss_ratio > MAX_BREMSSTRAHLUNG_LOSS_RATIO:
        flaws.append(
            f"Bremsstrahlung radiation loss ratio {bremsstrahlung_loss_ratio:.3f} exceeds thermal ceiling "
            f"{MAX_BREMSSTRAHLUNG_LOSS_RATIO:.2f}."
        )

    return BussardRamjetValidationResult(
        is_valid=len(flaws) == 0,
        scoop_radius_km=scoop_radius_km,
        flight_velocity_beta=flight_velocity_beta,
        magnetic_scoop_field_t=magnetic_scoop_field_t,
        photo_ionization_efficiency=photo_ionization_efficiency,
        capture_cross_section_efficiency=capture_cross_section_efficiency,
        thrust_to_drag_ratio=thrust_to_drag_ratio,
        exhaust_velocity_m_s=exhaust_velocity_m_s,
        nozzle_collimation_efficiency=nozzle_collimation_efficiency,
        ship_acceleration_m_s2=ship_acceleration_m_s2,
        core_fusion_temp_k=core_fusion_temp_k,
        bremsstrahlung_loss_ratio=bremsstrahlung_loss_ratio,
        flaws=flaws
    )
