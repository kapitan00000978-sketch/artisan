"""Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Reference Equations.

Formulated by Dr. Silas 'The Wave' Sterling,
Principal Extreme Non-Linear Ocean Wave & Rogue Wave Hydrodynamics Architect.
"""

from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional, Tuple


# Quantitative Physical Constants & Hydrodynamic Invariants
MIN_BENJAMIN_FEIR_INDEX: float = 1.0
MAX_BENJAMIN_FEIR_INDEX: float = 3.5
ROGUE_HEIGHT_RATIO_THRESHOLD: float = 2.0
CREST_ABNORMALITY_THRESHOLD: float = 1.25
MIN_WAVE_STEEPNESS: float = 0.10
MAX_WAVE_STEEPNESS_BREAKING: float = 0.44
MIN_SLAMMING_PRESSURE_KPA: float = 500.0
MIN_SURFACE_KURTOSIS: float = 3.0
MAX_DIRECTIONAL_SPREADING_DEG: float = 30.0
MIN_PEREGRINE_AMPLIFICATION: float = 2.50
MAX_PEREGRINE_AMPLIFICATION: float = 3.00
MIN_HOSM_NONLINEAR_ORDER: int = 3
MIN_DECK_AIRGAP_METERS: float = 2.0
MAX_DYNAMIC_AMPLIFICATION_FACTOR: float = 1.80
SEAWATER_DENSITY_KG_M3: float = 1025.0
GRAVITY_ACCELERATION: float = 9.80665


@dataclass
class ExtremeWaveValidationResult:
    """Hydrodynamic validation and compliance ledger."""
    is_valid: bool
    score: float
    violations: List[str] = field(default_factory=list)
    parameters: Dict[str, float] = field(default_factory=dict)
    remediation_notes: List[str] = field(default_factory=list)


def calculate_benjamin_feir_index(
    steepness: float,
    spectral_bandwidth: float
) -> float:
    """Compute the 1D Benjamin-Feir Index (BFI) for modulational wave instability.
    
    BFI = (epsilon * sqrt(2)) / (delta_omega / omega_0)
    """
    if spectral_bandwidth <= 0.0:
        raise ValueError("Spectral bandwidth delta_omega / omega_0 must be strictly positive.")
    if steepness <= 0.0:
        raise ValueError("Wave steepness epsilon must be strictly positive.")
    return (steepness * math.sqrt(2.0)) / spectral_bandwidth


def calculate_rogue_wave_criteria(
    h_max: float,
    eta_crest: float,
    h_s: float
) -> Tuple[float, float]:
    """Calculate wave height ratio H_max / H_s and crest abnormality index eta_crest / H_s."""
    if h_s <= 0.0:
        raise ValueError("Significant wave height H_s must be strictly positive.")
    height_ratio = h_max / h_s
    crest_ratio = eta_crest / h_s
    return height_ratio, crest_ratio


def calculate_wave_steepness(
    wavenumber_k: float,
    amplitude_a: float
) -> float:
    """Calculate non-linear wave steepness epsilon = k * a."""
    if wavenumber_k <= 0.0:
        raise ValueError("Wavenumber k must be strictly positive.")
    if amplitude_a <= 0.0:
        raise ValueError("Wave amplitude a must be strictly positive.")
    return wavenumber_k * amplitude_a


def calculate_slamming_pressure(
    impact_velocity: float,
    slamming_coefficient: float = 2.0 * math.pi,
    density_w: float = SEAWATER_DENSITY_KG_M3
) -> float:
    """Calculate Wagner peak hydrodynamic slamming impact pressure in kPa.
    
    P_slam = 0.5 * C_s * rho_w * v_impact^2  [Pa]
    Returns pressure in kilopascals (kPa).
    """
    if impact_velocity < 0.0:
        raise ValueError("Impact velocity must be non-negative.")
    if slamming_coefficient <= 0.0:
        raise ValueError("Slamming coefficient must be strictly positive.")
    pressure_pa = 0.5 * slamming_coefficient * density_w * (impact_velocity ** 2)
    return pressure_pa / 1000.0


def calculate_peregrine_breather_amplitude(
    a0: float,
    x: float = 0.0,
    t: float = 0.0,
    k0: float = 1.0,
    omega0: float = 1.0
) -> float:
    """Compute the envelope amplitude |psi(x,t)| of a 1D Peregrine breather soliton.
    
    Theoretical maximum amplification factor at (x=0, t=0) is exactly 3.0 * a0.
    """
    if a0 <= 0.0:
        raise ValueError("Background wave amplitude a0 must be strictly positive.")
    denom = 1.0 + 4.0 * (k0 ** 2) * (x ** 2) + 16.0 * (omega0 ** 2) * (t ** 2)
    re_psi = 1.0 - (4.0 * (1.0 + 4.0 * 1.0j * omega0 * t)) / denom
    envelope_amp = a0 * abs(re_psi)
    return float(envelope_amp)


def calculate_wave_in_deck_airgap(
    deck_height: float,
    eta_max: float
) -> float:
    """Calculate offshore platform deck bottom air gap clearance margin in meters."""
    return deck_height - eta_max


def validate_extreme_wave_parameters(
    benjamin_feir_index: float,
    rogue_height_ratio: float,
    crest_abnormality: float,
    steepness: float,
    slamming_pressure_kpa: float,
    kurtosis: float,
    directional_spreading_deg: float,
    hosm_order: int,
    deck_airgap_m: float,
    daf: float
) -> ExtremeWaveValidationResult:
    """Deterministically audit extreme wave hydrodynamic parameters against physical invariants."""
    violations: List[str] = []
    remediation_notes: List[str] = []
    deductions: float = 0.0

    params: Dict[str, float] = {
        "benjamin_feir_index": benjamin_feir_index,
        "rogue_height_ratio": rogue_height_ratio,
        "crest_abnormality": crest_abnormality,
        "steepness": steepness,
        "slamming_pressure_kpa": slamming_pressure_kpa,
        "kurtosis": kurtosis,
        "directional_spreading_deg": directional_spreading_deg,
        "hosm_order": float(hosm_order),
        "deck_airgap_m": deck_airgap_m,
        "daf": daf,
    }

    # 1. Benjamin-Feir Modulational Instability
    if benjamin_feir_index < MIN_BENJAMIN_FEIR_INDEX:
        violations.append(
            f"Benjamin-Feir Index {benjamin_feir_index:.2f} < {MIN_BENJAMIN_FEIR_INDEX:.2f}: "
            "Underestimating non-linear modulational instability and rogue wave focus."
        )
        remediation_notes.append("Elevate BFI >= 1.0 by accounting for narrow-banded spectral energy density.")
        deductions += 15.0

    # 2. Rogue Wave Height & Crest Criteria
    if rogue_height_ratio < ROGUE_HEIGHT_RATIO_THRESHOLD:
        violations.append(
            f"Rogue Wave Height Ratio {rogue_height_ratio:.2f} < {ROGUE_HEIGHT_RATIO_THRESHOLD:.2f}: "
            "Fails to meet international rogue wave threshold (H_max >= 2.0 * H_s)."
        )
        remediation_notes.append("Enforce rogue wave definition H_max >= 2.0 * H_s.")
        deductions += 15.0

    if crest_abnormality < CREST_ABNORMALITY_THRESHOLD:
        violations.append(
            f"Crest Abnormality Index {crest_abnormality:.2f} < {CREST_ABNORMALITY_THRESHOLD:.2f}: "
            "Crest elevation does not meet extreme non-linear asymmetric peaking criterion."
        )
        remediation_notes.append("Enforce crest abnormality index eta_crest / H_s >= 1.25.")
        deductions += 10.0

    # 3. Wave Steepness & Kinematic Breaking Limit
    if steepness > MAX_WAVE_STEEPNESS_BREAKING:
        violations.append(
            f"Wave Steepness {steepness:.3f} > {MAX_WAVE_STEEPNESS_BREAKING:.2f}: "
            "Exceeds Stokes kinematic wave breaking threshold ka = 0.44."
        )
        remediation_notes.append("Apply non-linear kinematic breaking energy dissipation filter.")
        deductions += 20.0
    elif steepness < MIN_WAVE_STEEPNESS:
        violations.append(
            f"Wave Steepness {steepness:.3f} < {MIN_WAVE_STEEPNESS:.2f}: "
            "Wave steepness too mild to sustain non-linear four-wave interactions."
        )
        remediation_notes.append("Ensure realistic steep sea state ka >= 0.10.")
        deductions += 10.0

    # 4. Wave Slamming Impact Pressure
    if slamming_pressure_kpa < MIN_SLAMMING_PRESSURE_KPA:
        violations.append(
            f"Slamming Pressure {slamming_pressure_kpa:.1f} kPa < {MIN_SLAMMING_PRESSURE_KPA:.1f} kPa: "
            "Under-predicting hydrodynamic wave impact loads on marine structures."
        )
        remediation_notes.append("Incorporate Wagner hydrodynamic slamming coefficient C_s >= 2*pi.")
        deductions += 15.0

    # 5. Surface Elevation Kurtosis
    if kurtosis < MIN_SURFACE_KURTOSIS:
        violations.append(
            f"Surface Kurtosis {kurtosis:.2f} < {MIN_SURFACE_KURTOSIS:.2f}: "
            "Sub-Gaussian distribution ignores heavy-tail non-linear rogue probability."
        )
        remediation_notes.append("Model non-Gaussian heavy tail with kurtosis K >= 3.0.")
        deductions += 10.0

    # 6. Directional Spectral Spreading
    if directional_spreading_deg > MAX_DIRECTIONAL_SPREADING_DEG:
        violations.append(
            f"Directional Spreading {directional_spreading_deg:.1f} deg > {MAX_DIRECTIONAL_SPREADING_DEG:.1f} deg: "
            "Broad spreading diffuses quasi-1D modulational rogue amplification."
        )
        remediation_notes.append("Focus directional spreading sigma_theta <= 30.0 deg for coherent packet growth.")
        deductions += 10.0

    # 7. High-Order Spectral Method Order
    if hosm_order < MIN_HOSM_NONLINEAR_ORDER:
        violations.append(
            f"HOSM Order {hosm_order} < {MIN_HOSM_NONLINEAR_ORDER}: "
            "Cannot capture resonant four-wave non-linear interactions without order >= 3."
        )
        remediation_notes.append("Increase HOSM expansion order to at least M = 3.")
        deductions += 15.0

    # 8. Deck Air Gap Clearance
    if deck_airgap_m < MIN_DECK_AIRGAP_METERS:
        violations.append(
            f"Deck Air Gap {deck_airgap_m:.2f} m < {MIN_DECK_AIRGAP_METERS:.2f} m: "
            "Negative or insufficient air gap risks catastrophic wave-in-deck inundation."
        )
        remediation_notes.append("Elevate platform cellar deck to maintain air gap >= 2.0 m.")
        deductions += 20.0

    # 9. Dynamic Amplification Factor
    if daf > MAX_DYNAMIC_AMPLIFICATION_FACTOR:
        violations.append(
            f"Dynamic Amplification Factor {daf:.2f} > {MAX_DYNAMIC_AMPLIFICATION_FACTOR:.2f}: "
            "Structural resonant magnification exceeds safe operational bounds."
        )
        remediation_notes.append("Damp structural response to enforce DAF <= 1.80.")
        deductions += 10.0

    score = max(0.0, 100.0 - deductions)
    is_valid = (score >= 95.0) and (len(violations) == 0)

    return ExtremeWaveValidationResult(
        is_valid=is_valid,
        score=score,
        violations=violations,
        parameters=params,
        remediation_notes=remediation_notes
    )
