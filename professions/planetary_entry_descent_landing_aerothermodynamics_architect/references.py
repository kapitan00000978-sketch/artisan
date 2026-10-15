"""Planetary Atmospheric Entry, Descent & Landing (EDL) Reference Equations.

Formulated by Dr. Caelum 'The Exosphere' Sterling,
Principal Planetary Atmospheric Entry, Descent & Landing (EDL) Aerothermodynamics Architect.
"""

from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional, Tuple


# Quantitative Aerothermodynamic Constants & Physical Bounds
MIN_ENTRY_VELOCITY_KM_S: float = 5.5
MAX_ENTRY_VELOCITY_KM_S: float = 12.5
MIN_ENTRY_MACH: float = 25.0
MIN_STAGNATION_HEAT_FLUX_MW_M2: float = 4.50
MIN_TOTAL_HEAT_LOAD_MJ_M2: float = 120.0
MIN_TPS_SAFETY_FACTOR: float = 1.50
MAX_BONDLINE_TEMP_C: float = 250.0
MAX_PEAK_DECELERATION_G: float = 15.0
MIN_PARACHUTE_DEPLOY_MACH: float = 1.40
MAX_PARACHUTE_DEPLOY_MACH: float = 2.20
MIN_PARACHUTE_DYNAMIC_PRESSURE_PA: float = 300.0
MAX_PARACHUTE_DYNAMIC_PRESSURE_PA: float = 950.0
MIN_TRN_ALTITUDE_M: float = 2500.0
MAX_LANDING_ELLIPSE_SEMI_MAJOR_M: float = 50.0
MAX_TOUCHDOWN_VERTICAL_VELOCITY_M_S: float = 0.75
MAX_TOUCHDOWN_HORIZONTAL_VELOCITY_M_S: float = 0.15
MIN_PLASMA_RF_MARGIN_DB: float = 10.0
STANDARD_GRAVITY: float = 9.80665


@dataclass
class EDLAerothermodynamicsValidationResult:
    """Diagnostic ledger and certification report for EDL mission architectures."""
    is_valid: bool
    score: float
    violations: List[str] = field(default_factory=list)
    parameters: Dict[str, float] = field(default_factory=dict)
    remediation_notes: List[str] = field(default_factory=list)


def calculate_sutton_graves_stagnation_heat_flux(
    nose_radius_m: float,
    density_inf_kg_m3: float,
    velocity_m_s: float,
    k_sg: float = 1.7415e-4
) -> float:
    """Calculate convective stagnation point heat flux in MW/m^2 via Sutton-Graves relation.
    
    q_stag = k_sg * sqrt(rho_inf / R_nose) * v^3  [W/m^2]
    Returns heat flux in megawatts per square meter (MW/m^2).
    """
    if nose_radius_m <= 0.0:
        raise ValueError("Nose radius must be strictly positive.")
    if density_inf_kg_m3 < 0.0:
        raise ValueError("Freestream atmospheric density cannot be negative.")
    if velocity_m_s < 0.0:
        raise ValueError("Entry velocity must be non-negative.")
    q_watts_m2 = k_sg * math.sqrt(density_inf_kg_m3 / nose_radius_m) * (velocity_m_s ** 3)
    return q_watts_m2 / 1.0e6


def calculate_integrated_heat_load(
    avg_heat_flux_mw_m2: float,
    pulse_duration_s: float
) -> float:
    """Calculate integrated thermal entry heat load Q_total in MJ/m^2."""
    if avg_heat_flux_mw_m2 <= 0.0 or pulse_duration_s <= 0.0:
        raise ValueError("Heat flux and duration must be strictly positive.")
    return avg_heat_flux_mw_m2 * pulse_duration_s


def calculate_supersonic_dynamic_pressure(
    density_kg_m3: float,
    velocity_m_s: float
) -> float:
    """Calculate dynamic pressure q = 0.5 * rho * v^2 in Pascals (Pa)."""
    if density_kg_m3 < 0.0 or velocity_m_s < 0.0:
        raise ValueError("Density and velocity must be non-negative.")
    return 0.5 * density_kg_m3 * (velocity_m_s ** 2)


def calculate_terminal_touchdown_energy(
    lander_mass_kg: float,
    v_vertical_m_s: float,
    v_horizontal_m_s: float
) -> float:
    """Calculate residual kinetic energy at touchdown in Joules."""
    if lander_mass_kg <= 0.0:
        raise ValueError("Lander mass must be strictly positive.")
    v_total_sq = (v_vertical_m_s ** 2) + (v_horizontal_m_s ** 2)
    return 0.5 * lander_mass_kg * v_total_sq


def calculate_parachute_drag_force(
    cd: float,
    reference_area_m2: float,
    dynamic_pressure_pa: float
) -> float:
    """Calculate aerodynamic parachute drag force in Newtons: F_drag = C_D * A * q."""
    if cd <= 0.0 or reference_area_m2 <= 0.0 or dynamic_pressure_pa < 0.0:
        raise ValueError("Parachute parameters must be positive.")
    return cd * reference_area_m2 * dynamic_pressure_pa


def validate_edl_parameters(
    entry_velocity_km_s: float,
    stagnation_heat_flux_mw_m2: float,
    total_heat_load_mj_m2: float,
    tps_safety_factor: float,
    bondline_temp_c: float,
    peak_deceleration_g: float,
    parachute_deploy_mach: float,
    parachute_dynamic_pressure_pa: float,
    landing_ellipse_semi_major_m: float,
    touchdown_vz_m_s: float
) -> EDLAerothermodynamicsValidationResult:
    """Audit EDL aerothermodynamic and trajectory parameters against physical invariants."""
    violations: List[str] = []
    remediation_notes: List[str] = []
    deductions: float = 0.0

    params: Dict[str, float] = {
        "entry_velocity_km_s": entry_velocity_km_s,
        "stagnation_heat_flux_mw_m2": stagnation_heat_flux_mw_m2,
        "total_heat_load_mj_m2": total_heat_load_mj_m2,
        "tps_safety_factor": tps_safety_factor,
        "bondline_temp_c": bondline_temp_c,
        "peak_deceleration_g": peak_deceleration_g,
        "parachute_deploy_mach": parachute_deploy_mach,
        "parachute_dynamic_pressure_pa": parachute_dynamic_pressure_pa,
        "landing_ellipse_semi_major_m": landing_ellipse_semi_major_m,
        "touchdown_vz_m_s": touchdown_vz_m_s,
    }

    # 1. Entry Velocity Envelope
    if entry_velocity_km_s < MIN_ENTRY_VELOCITY_KM_S or entry_velocity_km_s > MAX_ENTRY_VELOCITY_KM_S:
        violations.append(
            f"Entry Velocity {entry_velocity_km_s:.2f} km/s outside certified planetary envelope [{MIN_ENTRY_VELOCITY_KM_S}, {MAX_ENTRY_VELOCITY_KM_S}] km/s."
        )
        remediation_notes.append("Target hyperbolic atmospheric entry interface within [5.5, 12.5] km/s.")
        deductions += 15.0

    # 2. Stagnation Heat Flux & Integrated Thermal Load
    if stagnation_heat_flux_mw_m2 < MIN_STAGNATION_HEAT_FLUX_MW_M2:
        violations.append(
            f"Stagnation Heat Flux {stagnation_heat_flux_mw_m2:.2f} MW/m^2 < {MIN_STAGNATION_HEAT_FLUX_MW_M2:.2f} MW/m^2: "
            "Underestimating hypersonic shock-layer convective/radiative heating."
        )
        remediation_notes.append("Incorporate full real-gas Sutton-Graves / Fay-Riddell heat flux modeling.")
        deductions += 15.0

    if total_heat_load_mj_m2 < MIN_TOTAL_HEAT_LOAD_MJ_M2:
        violations.append(
            f"Total Heat Load {total_heat_load_mj_m2:.1f} MJ/m^2 < {MIN_TOTAL_HEAT_LOAD_MJ_M2:.1f} MJ/m^2: "
            "Integrated atmospheric thermal pulse underestimated."
        )
        remediation_notes.append("Integrate entry heating pulse across full hypersonic trajectory.")
        deductions += 10.0

    # 3. TPS Safety Factor & Bondline Temperature
    if tps_safety_factor < MIN_TPS_SAFETY_FACTOR:
        violations.append(
            f"TPS Safety Factor {tps_safety_factor:.2f} < {MIN_TPS_SAFETY_FACTOR:.2f}: "
            "Heatshield ablation margin breaches aerospace certification standard."
        )
        remediation_notes.append("Thicken ablative PICA/PICA-X heatshield to guarantee SF >= 1.50.")
        deductions += 20.0

    if bondline_temp_c > MAX_BONDLINE_TEMP_C:
        violations.append(
            f"Bondline Temperature {bondline_temp_c:.1f} C > {MAX_BONDLINE_TEMP_C:.1f} C: "
            "Adhesive pyrolytic decomposition risks structural capsule heatshield loss."
        )
        remediation_notes.append("Enforce structural composite bondline temperature T_bond <= 250.0 C.")
        deductions += 20.0

    # 4. Deceleration G-Load
    if peak_deceleration_g > MAX_PEAK_DECELERATION_G:
        violations.append(
            f"Peak Deceleration {peak_deceleration_g:.1f} g > {MAX_PEAK_DECELERATION_G:.1f} g: "
            "Structural and scientific payload acceleration limit breached."
        )
        remediation_notes.append("Shallow entry flight path angle gamma to constrain deceleration <= 15.0 g.")
        deductions += 15.0

    # 5. Parachute Deployment Mach & Dynamic Pressure
    if parachute_deploy_mach < MIN_PARACHUTE_DEPLOY_MACH or parachute_deploy_mach > MAX_PARACHUTE_DEPLOY_MACH:
        violations.append(
            f"Parachute Deploy Mach {parachute_deploy_mach:.2f} outside safe supersonic window [{MIN_PARACHUTE_DEPLOY_MACH}, {MAX_PARACHUTE_DEPLOY_MACH}]."
        )
        remediation_notes.append("Trigger supersonic parachute mortar strictly between Mach 1.40 and 2.20.")
        deductions += 15.0

    if parachute_dynamic_pressure_pa < MIN_PARACHUTE_DYNAMIC_PRESSURE_PA or parachute_dynamic_pressure_pa > MAX_PARACHUTE_DYNAMIC_PRESSURE_PA:
        violations.append(
            f"Parachute Dynamic Pressure {parachute_dynamic_pressure_pa:.1f} Pa outside certified canopy envelope [{MIN_PARACHUTE_DYNAMIC_PRESSURE_PA}, {MAX_PARACHUTE_DYNAMIC_PRESSURE_PA}] Pa."
        )
        remediation_notes.append("Deploy canopy within certified dynamic pressure limits [300.0, 950.0] Pa.")
        deductions += 10.0

    # 6. Terrain-Relative Navigation Landing Accuracy
    if landing_ellipse_semi_major_m > MAX_LANDING_ELLIPSE_SEMI_MAJOR_M:
        violations.append(
            f"Landing Ellipse {landing_ellipse_semi_major_m:.1f} m > {MAX_LANDING_ELLIPSE_SEMI_MAJOR_M:.1f} m: "
            "Target precision fails pinpoint landing standard."
        )
        remediation_notes.append("Engage optical TRN landmark matching to tighten landing ellipse <= 50.0 m.")
        deductions += 15.0

    # 7. Terminal Touchdown Vertical Velocity
    if touchdown_vz_m_s > MAX_TOUCHDOWN_VERTICAL_VELOCITY_M_S:
        violations.append(
            f"Touchdown Velocity {touchdown_vz_m_s:.2f} m/s > {MAX_TOUCHDOWN_VERTICAL_VELOCITY_M_S:.2f} m/s: "
            "Excessive vertical impact velocity risks gear collapse."
        )
        remediation_notes.append("Throttle terminal retro-rockets to constrain touchdown vz <= 0.75 m/s.")
        deductions += 20.0

    score = max(0.0, 100.0 - deductions)
    is_valid = (score >= 95.0) and (len(violations) == 0)

    return EDLAerothermodynamicsValidationResult(
        is_valid=is_valid,
        score=score,
        violations=violations,
        parameters=params,
        remediation_notes=remediation_notes
    )
