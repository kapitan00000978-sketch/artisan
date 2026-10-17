"""Planetary Geodynamo Core Fluid Dynamics Reference Specifications and Quantitative Equations.

Embodying the domain standards of Dr. Lyra 'The Core' Sterling:
Magnetostrophic MAC Balance, Magnetic Reynolds induction threshold, Core-Mantle
Boundary (CMB) convective heat flux, Inner Core Boundary (ICB) light-element
compositional buoyancy flux, and geomagnetic dipole field stability.
"""

from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional


# Fundamental Physical & Geophysical Constants for Earth's Core
EARTH_ROTATION_RATE_RAD_S = 7.292115e-5  # Earth angular velocity Omega (rad/s)
OUTER_CORE_SHELL_THICKNESS_M = 2.2585e6  # Shell thickness L = r_CMB - r_ICB (m)
OUTER_CORE_MEAN_DENSITY_KG_M3 = 1.1e4    # Liquid iron core density rho (kg/m^3)
CORE_ELECTRICAL_CONDUCTIVITY_S_M = 1.0e6 # Liquid Fe-Ni conductivity sigma (S/m)
VACUUM_PERMEABILITY_H_M = 4.0 * math.pi * 1e-7 # mu_0 (H/m)
CORE_MAGNETIC_DIFFUSIVITY_M2_S = 1.0 / (VACUUM_PERMEABILITY_H_M * CORE_ELECTRICAL_CONDUCTIVITY_S_M) # ~0.796 m^2/s

# Quantitative Boundaries
MIN_MAGNETIC_REYNOLDS = 50.0
MAX_ROSSBY_NUMBER = 1.0e-6
MAX_EKMAN_NUMBER = 1.0e-14
MIN_ELSASSER_NUMBER = 0.10
MAX_ELSASSER_NUMBER = 10.0
MIN_CMB_HEAT_FLUX_TW = 10.0
MIN_ICB_BUOYANCY_FLUX_KG_S = 1.0e5
MIN_SURFACE_DIPOLE_UT = 25.0
MAX_SURFACE_DIPOLE_UT = 65.0
MIN_CMB_MAGNETIC_FIELD_MT = 0.50
MIN_SURFACE_DIPOLE_FRACTION = 0.80
MAX_DIPOLE_TILT_DEG = 15.0
MAX_WESTWARD_DRIFT_DEG_YR = 0.30
MIN_DYNAMO_NUMBER = 100.0


def calculate_magnetic_reynolds_number(
    velocity: float,
    shell_thickness: float = OUTER_CORE_SHELL_THICKNESS_M,
    magnetic_diffusivity: float = CORE_MAGNETIC_DIFFUSIVITY_M2_S,
) -> float:
    """Calculate the Magnetic Reynolds number Rm = U * L / eta_mag."""
    if magnetic_diffusivity <= 0.0:
        raise ValueError("Magnetic diffusivity must be positive.")
    if velocity < 0.0 or shell_thickness <= 0.0:
        raise ValueError("Velocity and shell thickness must be non-negative and positive.")
    return (velocity * shell_thickness) / magnetic_diffusivity


def calculate_rossby_number(
    velocity: float,
    angular_velocity: float = EARTH_ROTATION_RATE_RAD_S,
    length_scale: float = OUTER_CORE_SHELL_THICKNESS_M,
) -> float:
    """Calculate the Rossby number Ro = U / (2 * Omega * L)."""
    denominator = 2.0 * angular_velocity * length_scale
    if denominator <= 0.0:
        raise ValueError("Angular velocity and length scale must be positive.")
    return velocity / denominator


def calculate_ekman_number(
    kinematic_viscosity: float,
    angular_velocity: float = EARTH_ROTATION_RATE_RAD_S,
    length_scale: float = OUTER_CORE_SHELL_THICKNESS_M,
) -> float:
    """Calculate the Ekman number Ek = nu / (2 * Omega * L^2)."""
    denominator = 2.0 * angular_velocity * (length_scale ** 2)
    if denominator <= 0.0:
        raise ValueError("Angular velocity and length scale must be positive.")
    return kinematic_viscosity / denominator


def calculate_elsasser_number(
    magnetic_field_tesla: float,
    electrical_conductivity: float = CORE_ELECTRICAL_CONDUCTIVITY_S_M,
    density: float = OUTER_CORE_MEAN_DENSITY_KG_M3,
    angular_velocity: float = EARTH_ROTATION_RATE_RAD_S,
) -> float:
    """Calculate the Elsasser number Lambda = sigma * B^2 / (2 * rho * Omega)."""
    denominator = 2.0 * density * angular_velocity
    if denominator <= 0.0:
        raise ValueError("Density and angular velocity must be positive.")
    return (electrical_conductivity * (magnetic_field_tesla ** 2)) / denominator


def calculate_surface_dipole_energy_fraction(
    dipole_energy: float,
    total_energy: float,
) -> float:
    """Calculate dipolar energy fraction f_dipole = E_dipole / E_total."""
    if total_energy <= 0.0:
        raise ValueError("Total magnetic field energy must be positive.")
    if dipole_energy < 0.0 or dipole_energy > total_energy:
        raise ValueError("Dipole energy must be non-negative and <= total energy.")
    return dipole_energy / total_energy


def calculate_dynamo_number(
    alpha_effect_m_s: float,
    omega_shear_rad_s: float,
    length_scale: float = OUTER_CORE_SHELL_THICKNESS_M,
    magnetic_diffusivity: float = CORE_MAGNETIC_DIFFUSIVITY_M2_S,
) -> float:
    """Calculate the dimensionless dynamo number N_D = (alpha * Delta_Omega * L^3) / eta^2."""
    if magnetic_diffusivity <= 0.0:
        raise ValueError("Magnetic diffusivity must be positive.")
    return abs(alpha_effect_m_s * omega_shear_rad_s * (length_scale ** 3)) / (magnetic_diffusivity ** 2)


@dataclass
class GeodynamoCoreParameters:
    """Quantitative parameters defining outer core geodynamo fluid and magnetic state."""
    magnetic_reynolds: float
    rossby_number: float
    ekman_number: float
    elsasser_number: float
    cmb_heat_flux_tw: float
    icb_buoyancy_flux_kg_s: float
    surface_dipole_field_microtesla: float
    cmb_magnetic_field_millitesla: float
    surface_dipole_fraction: float
    dipole_tilt_deg: float
    westward_drift_deg_yr: float
    dynamo_number_product: float


@dataclass
class GeodynamoValidationResult:
    """Validation report generated by Dr. Lyra Sterling's geodynamo invariants."""
    is_valid: bool
    violations: List[str] = field(default_factory=list)
    score: float = 100.0
    metrics: Dict[str, float] = field(default_factory=dict)


def validate_geodynamo_parameters(params: GeodynamoCoreParameters) -> GeodynamoValidationResult:
    """Validate planetary geodynamo core parameters against strict magnetohydrodynamic invariants."""
    violations: List[str] = []
    deductions: float = 0.0

    # 1. Magnetic Reynolds induction threshold
    if params.magnetic_reynolds < MIN_MAGNETIC_REYNOLDS:
        violations.append(
            f"Magnetic Reynolds number sub-critical: {params.magnetic_reynolds:.2f} < {MIN_MAGNETIC_REYNOLDS:.1f}. "
            "Magnetic diffusion dominates convective induction; dynamo decay is inevitable."
        )
        deductions += 25.0

    # 2. Rossby number Coriolis dominance
    if params.rossby_number > MAX_ROSSBY_NUMBER:
        violations.append(
            f"Rossby number breaches Coriolis limit: {params.rossby_number:.2e} > {MAX_ROSSBY_NUMBER:.2e}. "
            "Inertia overpowers planetary rotation; geostrophic Taylor column alignment destroyed."
        )
        deductions += 15.0

    # 3. Ekman number vanishing viscosity
    if params.ekman_number > MAX_EKMAN_NUMBER:
        violations.append(
            f"Ekman number unphysically high: {params.ekman_number:.2e} > {MAX_EKMAN_NUMBER:.2e}. "
            "Molecular or artificial viscosity excessively damps magnetohydrodynamic outer core flow."
        )
        deductions += 15.0

    # 4. Elsasser number order-one confinement
    if not (MIN_ELSASSER_NUMBER <= params.elsasser_number <= MAX_ELSASSER_NUMBER):
        violations.append(
            f"Elsasser number out of magnetostrophic bounds: {params.elsasser_number:.2f} "
            f"not in [{MIN_ELSASSER_NUMBER:.2f}, {MAX_ELSASSER_NUMBER:.2f}]. MAC balance disrupted."
        )
        deductions += 15.0

    # 5. Core-Mantle Boundary heat flux
    if params.cmb_heat_flux_tw < MIN_CMB_HEAT_FLUX_TW:
        violations.append(
            f"CMB heat flux sub-adiabatic: {params.cmb_heat_flux_tw:.2f} TW < {MIN_CMB_HEAT_FLUX_TW:.1f} TW. "
            "Thermal convection insufficient to drive geodynamo."
        )
        deductions += 15.0

    # 6. Inner Core Boundary light-element buoyancy flux
    if params.icb_buoyancy_flux_kg_s < MIN_ICB_BUOYANCY_FLUX_KG_S:
        violations.append(
            f"ICB compositional buoyancy flux too weak: {params.icb_buoyancy_flux_kg_s:.2e} kg/s < {MIN_ICB_BUOYANCY_FLUX_KG_S:.2e} kg/s. "
            "Compositional plume driving insufficient to sustain convection."
        )
        deductions += 10.0

    # 7. Surface dipole field envelope
    if not (MIN_SURFACE_DIPOLE_UT <= params.surface_dipole_field_microtesla <= MAX_SURFACE_DIPOLE_UT):
        violations.append(
            f"Surface dipole field out of bounds: {params.surface_dipole_field_microtesla:.2f} uT "
            f"not in [{MIN_SURFACE_DIPOLE_UT:.1f}, {MAX_SURFACE_DIPOLE_UT:.1f}] uT."
        )
        deductions += 10.0

    # 8. CMB magnetic field RMS
    if params.cmb_magnetic_field_millitesla < MIN_CMB_MAGNETIC_FIELD_MT:
        violations.append(
            f"CMB magnetic field too weak: {params.cmb_magnetic_field_millitesla:.3f} mT < {MIN_CMB_MAGNETIC_FIELD_MT:.3f} mT."
        )
        deductions += 10.0

    # 9. Surface dipolar energy fraction
    if params.surface_dipole_fraction < MIN_SURFACE_DIPOLE_FRACTION:
        violations.append(
            f"Surface dipole fraction too low: {params.surface_dipole_fraction * 100:.1f}% < {MIN_SURFACE_DIPOLE_FRACTION * 100:.1f}%. "
            "Multipole noise obscures stable axial geomagnetic dipole."
        )
        deductions += 10.0

    # 10. Dipole tilt offset
    if params.dipole_tilt_deg > MAX_DIPOLE_TILT_DEG:
        violations.append(
            f"Dipole tilt excessive: {params.dipole_tilt_deg:.1f} deg > {MAX_DIPOLE_TILT_DEG:.1f} deg. "
            "Geomagnetic axis misaligned from planetary spin axis."
        )
        deductions += 5.0

    # 11. Secular westward drift rate
    if params.westward_drift_deg_yr > MAX_WESTWARD_DRIFT_DEG_YR:
        violations.append(
            f"Westward secular drift excessive: {params.westward_drift_deg_yr:.2f} deg/yr > {MAX_WESTWARD_DRIFT_DEG_YR:.2f} deg/yr."
        )
        deductions += 5.0

    # 12. Dynamo number product
    if params.dynamo_number_product < MIN_DYNAMO_NUMBER:
        violations.append(
            f"Dynamo number product sub-critical: {params.dynamo_number_product:.1f} < {MIN_DYNAMO_NUMBER:.1f}."
        )
        deductions += 5.0

    final_score = max(0.0, 100.0 - deductions)
    is_valid = len(violations) == 0

    metrics = {
        "magnetic_reynolds": params.magnetic_reynolds,
        "rossby_number": params.rossby_number,
        "ekman_number": params.ekman_number,
        "elsasser_number": params.elsasser_number,
        "cmb_heat_flux_tw": params.cmb_heat_flux_tw,
        "icb_buoyancy_flux_kg_s": params.icb_buoyancy_flux_kg_s,
        "surface_dipole_field_microtesla": params.surface_dipole_field_microtesla,
        "cmb_magnetic_field_millitesla": params.cmb_magnetic_field_millitesla,
        "surface_dipole_fraction": params.surface_dipole_fraction,
        "dipole_tilt_deg": params.dipole_tilt_deg,
        "westward_drift_deg_yr": params.westward_drift_deg_yr,
        "dynamo_number_product": params.dynamo_number_product,
    }

    return GeodynamoValidationResult(
        is_valid=is_valid,
        violations=violations,
        score=final_score,
        metrics=metrics,
    )
