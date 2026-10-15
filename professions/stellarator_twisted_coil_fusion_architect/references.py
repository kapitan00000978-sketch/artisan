"""Physical references and mathematical models for Stellarator Magnet & Non-Planar Twisted Coil Fusion.

Architect: Dr. Hector 'The Stellar' Vance
Domain: stellarator_twisted_coil_fusion_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Fundamental physical constants
VACUUM_PERMEABILITY: float = 4.0 * math.pi * 1.0e-7  # H/m (T*m/A)
BOLTZMANN_CONSTANT: float = 1.380649e-23           # J/K
ELEMENTARY_CHARGE: float = 1.602176634e-19         # C

# Core quantitative engineering thresholds for stellarator fusion reactors
MIN_ROTATIONAL_TRANSFORM: float = 0.80             # iota / 2pi >= 0.80
MAX_ROTATIONAL_TRANSFORM: float = 1.25             # iota / 2pi <= 1.25
MAX_MAGNETIC_SHEAR: float = 0.15                   # |s| <= 0.15
MIN_COIL_BEND_RADIUS_M: float = 0.50               # rho_bend >= 0.50 m (kappa <= 2.0 m^-1)
MAX_COIL_CURVATURE_M_INV: float = 2.0              # kappa <= 2.0 m^-1
MIN_COIL_PLASMA_STANDOFF_M: float = 1.20           # Delta_cp >= 1.20 m (blanket + shield + cryostat)
MAX_EFFECTIVE_HELICAL_RIPPLE: float = 0.010        # epsilon_eff^(3/2) <= 1.0% (0.010)
MAX_DIVERTOR_HEAT_FLUX_MW_M2: float = 10.0         # q_div <= 10.0 MW/m^2
MIN_DIVERTOR_RAD_FRACTION: float = 0.85            # f_rad >= 85%
MAX_ON_CONDUCTOR_PEAK_FIELD_T: float = 16.0        # B_peak <= 16.0 T
MAX_CASING_VON_MISES_MPA: float = 650.0            # sigma_vm <= 650.0 MPa
MAX_HTS_WINDING_STRAIN_PCT: float = 0.35           # epsilon_strain <= 0.35%
MAX_QUENCH_DUMP_TIME_MS: float = 250.0             # t_dump <= 250.0 ms
MAX_NET_TOROIDAL_CURRENT_KA: float = 50.0          # |I_p| <= 50.0 kA (steady-state disruption immunity)

# Critical low-order rational resonance forbidden values in core confinement volume
FORBIDDEN_CORE_RATIONALS: Tuple[float, ...] = (
    5.0 / 6.0,  # ~0.8333
    1.0 / 1.0,  # 1.0000
    5.0 / 5.0,  # 1.0000
    4.0 / 3.0   # ~1.3333
)


def calculate_rotational_transform(
    poloidal_turns: float,
    toroidal_turns: float
) -> float:
    """Calculate the rotational transform (iota / 2pi) across magnetic flux surfaces.

    iota / 2pi = Delta_theta / Delta_phi
    """
    if toroidal_turns <= 0.0:
        return 0.0
    return poloidal_turns / toroidal_turns


def calculate_coil_bend_curvature(
    dx: float,
    dy: float,
    dz: float,
    d2x: float,
    d2y: float,
    d2z: float
) -> Tuple[float, float]:
    """Calculate Frenet-Serret 3D space curve curvature kappa and bend radius rho.

    kappa = |r' x r''| / |r'|^3
    rho = 1 / kappa
    """
    v_norm_sq = (dx ** 2) + (dy ** 2) + (dz ** 2)
    v_norm = math.sqrt(v_norm_sq)
    if v_norm < 1.0e-9:
        return 0.0, float("inf")

    # Cross product r' x r''
    cx = (dy * d2z) - (dz * d2y)
    cy = (dz * d2x) - (dx * d2z)
    cz = (dx * d2y) - (dy * d2x)
    cross_norm = math.sqrt((cx ** 2) + (cy ** 2) + (cz ** 2))

    curvature = cross_norm / (v_norm ** 3)
    bend_radius = 1.0 / curvature if curvature > 1.0e-9 else float("inf")
    return curvature, bend_radius


def calculate_island_divertor_heat_flux(
    p_exhaust_mw: float,
    radiation_fraction: float,
    wetted_area_m2: float
) -> float:
    """Calculate peak target heat flux on island divertor plates in MW/m^2.

    q_div = (P_exhaust * (1 - f_rad)) / A_wetted
    """
    if wetted_area_m2 <= 0.0:
        return float("inf")
    unradiated_fraction = max(0.0, 1.0 - min(1.0, max(0.0, radiation_fraction)))
    return (max(0.0, p_exhaust_mw) * unradiated_fraction) / wetted_area_m2


def calculate_effective_ripple_transport_factor(
    effective_ripple: float,
    temperature_kev: float,
    magnetic_field_t: float
) -> float:
    """Calculate 1/nu regime neoclassical radial transport factor scaling.

    D_neo ~ (epsilon_eff^(3/2) * T_kev^(7/2)) / B^2
    """
    if magnetic_field_t <= 0.0 or effective_ripple < 0.0:
        return 0.0
    return (effective_ripple * (max(0.0, temperature_kev) ** 3.5)) / (magnetic_field_t ** 2)


@dataclass
class StellaratorFusionValidationResult:
    """Structured validation report for Modular Stellarator Magnet & Coil Physics."""
    is_valid: bool
    rotational_transform: float
    magnetic_shear: float
    min_coil_bend_radius_m: float
    coil_plasma_standoff_m: float
    effective_helical_ripple: float
    divertor_heat_flux_mw_m2: float
    divertor_rad_fraction: float
    conductor_peak_field_t: float
    casing_von_mises_mpa: float
    hts_winding_strain_pct: float
    quench_dump_time_ms: float
    net_toroidal_current_ka: float
    flaws: List[str]


def validate_stellarator_fusion_parameters(
    rotational_transform: float = 0.95,
    magnetic_shear: float = 0.05,
    min_coil_bend_radius_m: float = 0.65,
    coil_plasma_standoff_m: float = 1.45,
    effective_helical_ripple: float = 0.0065,
    divertor_heat_flux_mw_m2: float = 7.5,
    divertor_rad_fraction: float = 0.88,
    conductor_peak_field_t: float = 13.8,
    casing_von_mises_mpa: float = 520.0,
    hts_winding_strain_pct: float = 0.22,
    quench_dump_time_ms: float = 180.0,
    net_toroidal_current_ka: float = 12.0
) -> StellaratorFusionValidationResult:
    """Validate stellarator magnetic cage parameters against Dr. Hector Vance's strict benchmarks."""
    flaws: List[str] = []

    if rotational_transform < MIN_ROTATIONAL_TRANSFORM or rotational_transform > MAX_ROTATIONAL_TRANSFORM:
        flaws.append(
            f"Rotational transform iota/2pi {rotational_transform:.4f} outside safe window "
            f"[{MIN_ROTATIONAL_TRANSFORM:.2f}, {MAX_ROTATIONAL_TRANSFORM:.2f}]."
        )

    # Check for proximity to destructive rational resonances (within 0.015 margin)
    for forbidden in FORBIDDEN_CORE_RATIONALS:
        if abs(rotational_transform - forbidden) < 0.015:
            flaws.append(
                f"Rotational transform {rotational_transform:.4f} dangerously close to low-order rational "
                f"island resonance {forbidden:.4f}."
            )
            break

    if abs(magnetic_shear) > MAX_MAGNETIC_SHEAR:
        flaws.append(
            f"Magnetic shear |s| {abs(magnetic_shear):.4f} exceeds low-shear threshold {MAX_MAGNETIC_SHEAR:.2f}."
        )

    if min_coil_bend_radius_m < MIN_COIL_BEND_RADIUS_M:
        flaws.append(
            f"Minimum coil bend radius {min_coil_bend_radius_m:.3f} m below allowable limit {MIN_COIL_BEND_RADIUS_M:.2f} m "
            f"(Curvature exceeds {MAX_COIL_CURVATURE_M_INV:.1f} m^-1, inducing superconductor delamination)."
        )

    if coil_plasma_standoff_m < MIN_COIL_PLASMA_STANDOFF_M:
        flaws.append(
            f"Coil-to-plasma standoff distance {coil_plasma_standoff_m:.2f} m below required radial clearance "
            f"{MIN_COIL_PLASMA_STANDOFF_M:.2f} m for tritium blanket and neutron shield build."
        )

    if effective_helical_ripple > MAX_EFFECTIVE_HELICAL_RIPPLE:
        flaws.append(
            f"Effective helical magnetic ripple {effective_helical_ripple:.4f} exceeds 1/nu transport cap "
            f"{MAX_EFFECTIVE_HELICAL_RIPPLE:.4f}."
        )

    if divertor_heat_flux_mw_m2 > MAX_DIVERTOR_HEAT_FLUX_MW_M2:
        flaws.append(
            f"Island divertor target heat flux {divertor_heat_flux_mw_m2:.2f} MW/m^2 exceeds thermal exhaustion limit "
            f"{MAX_DIVERTOR_HEAT_FLUX_MW_M2:.1f} MW/m^2."
        )

    if divertor_rad_fraction < MIN_DIVERTOR_RAD_FRACTION:
        flaws.append(
            f"Divertor impurity radiative fraction {divertor_rad_fraction * 100.0:.1f}% below minimum requirement "
            f"{MIN_DIVERTOR_RAD_FRACTION * 100.0:.1f}%."
        )

    if conductor_peak_field_t > MAX_ON_CONDUCTOR_PEAK_FIELD_T:
        flaws.append(
            f"Peak magnetic field on conductor {conductor_peak_field_t:.2f} T exceeds superconducting limit "
            f"{MAX_ON_CONDUCTOR_PEAK_FIELD_T:.1f} T."
        )

    if casing_von_mises_mpa > MAX_CASING_VON_MISES_MPA:
        flaws.append(
            f"Coil casing Von Mises stress {casing_von_mises_mpa:.1f} MPa exceeds yield margin "
            f"{MAX_CASING_VON_MISES_MPA:.1f} MPa."
        )

    if hts_winding_strain_pct > MAX_HTS_WINDING_STRAIN_PCT:
        flaws.append(
            f"HTS winding pack mechanical strain {hts_winding_strain_pct:.3f}% exceeds critical tape threshold "
            f"{MAX_HTS_WINDING_STRAIN_PCT:.2f}%."
        )

    if quench_dump_time_ms > MAX_QUENCH_DUMP_TIME_MS:
        flaws.append(
            f"Quench dump energy extraction time {quench_dump_time_ms:.1f} ms exceeds safety envelope "
            f"{MAX_QUENCH_DUMP_TIME_MS:.1f} ms."
        )

    if abs(net_toroidal_current_ka) > MAX_NET_TOROIDAL_CURRENT_KA:
        flaws.append(
            f"Net toroidal current |I_p| {abs(net_toroidal_current_ka):.1f} kA exceeds zero-current stellarator cap "
            f"{MAX_NET_TOROIDAL_CURRENT_KA:.1f} kA (risking current-driven kink/tearing disruptions)."
        )

    return StellaratorFusionValidationResult(
        is_valid=len(flaws) == 0,
        rotational_transform=rotational_transform,
        magnetic_shear=magnetic_shear,
        min_coil_bend_radius_m=min_coil_bend_radius_m,
        coil_plasma_standoff_m=coil_plasma_standoff_m,
        effective_helical_ripple=effective_helical_ripple,
        divertor_heat_flux_mw_m2=divertor_heat_flux_mw_m2,
        divertor_rad_fraction=divertor_rad_fraction,
        conductor_peak_field_t=conductor_peak_field_t,
        casing_von_mises_mpa=casing_von_mises_mpa,
        hts_winding_strain_pct=hts_winding_strain_pct,
        quench_dump_time_ms=quench_dump_time_ms,
        net_toroidal_current_ka=net_toroidal_current_ka,
        flaws=flaws
    )
