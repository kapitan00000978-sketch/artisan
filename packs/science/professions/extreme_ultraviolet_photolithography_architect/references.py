"""High-NA EUV Photolithography Reference Equations & Physical Invariants.

Formulated by Dr. Nadia 'The Sub-Micron' Vance,
Principal High-NA EUV Photolithography & Sub-2nm Semiconductor Patterning Architect.
"""

from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional, Tuple


# Physical & Lithographic Constants
EUV_WAVELENGTH_NM: float = 13.5
MAX_EUV_BANDWIDTH_NM: float = 0.27
MIN_HIGH_NA: float = 0.55
MIN_K1_FACTOR: float = 0.30
MAX_RAYLEIGH_HALF_PITCH_NM: float = 8.0
MAX_LWR_3SIGMA_NM: float = 1.20
MAX_LER_3SIGMA_NM: float = 0.85
MIN_PHOTON_DENSITY_PER_NM2: float = 10.0
MIN_DOSE_TO_SIZE_MJ_CM2: float = 30.0
MAX_DOSE_TO_SIZE_MJ_CM2: float = 75.0
MAX_OVERLAY_ERROR_NM: float = 1.10
MAX_CDU_3SIGMA_NM: float = 0.60
MIN_PELLICLE_TRANSMISSION: float = 0.90
MIN_PELLICLE_THERMAL_WATTS: float = 600.0
MIN_LPP_CONVERSION_EFFICIENCY: float = 0.05
MIN_TIN_DROPLET_FREQ_KHZ: float = 50.0
MIN_LASER_POWER_KW: float = 30.0
PLANCK_CONSTANT_EV_S: float = 4.135667696e-15
SPEED_OF_LIGHT_M_S: float = 299792458.0
ELECTRON_VOLT_TO_JOULE: float = 1.602176634e-19


@dataclass
class EUVLithographyValidationResult:
    """Lithographic compliance ledger and diagnostic report."""
    is_valid: bool
    score: float
    violations: List[str] = field(default_factory=list)
    parameters: Dict[str, float] = field(default_factory=dict)
    remediation_notes: List[str] = field(default_factory=list)


def calculate_euv_photon_energy_ev(wavelength_nm: float = EUV_WAVELENGTH_NM) -> float:
    """Calculate single EUV photon energy in electron volts (eV).
    
    E = (h * c) / lambda ~ 91.8 eV for 13.5 nm.
    """
    if wavelength_nm <= 0.0:
        raise ValueError("EUV wavelength must be strictly positive.")
    wavelength_m = wavelength_nm * 1e-9
    energy_joules = (PLANCK_CONSTANT_EV_S * ELECTRON_VOLT_TO_JOULE * SPEED_OF_LIGHT_M_S) / wavelength_m
    return energy_joules / ELECTRON_VOLT_TO_JOULE


def calculate_rayleigh_resolution(
    wavelength_nm: float,
    na: float,
    k1: float = MIN_K1_FACTOR
) -> float:
    """Calculate Rayleigh half-pitch resolution in nanometers: HP = k1 * (lambda / NA)."""
    if na <= 0.0:
        raise ValueError("Numerical aperture NA must be strictly positive.")
    if k1 <= 0.0:
        raise ValueError("Process difficulty factor k1 must be strictly positive.")
    return k1 * (wavelength_nm / na)


def calculate_photon_density_per_nm2(
    dose_mj_cm2: float,
    wavelength_nm: float = EUV_WAVELENGTH_NM
) -> float:
    """Calculate incident photon count per square nanometer from exposure dose in mJ/cm^2.
    
    1 mJ/cm^2 = 1e-3 J / 1e14 nm^2 = 1e-17 J/nm^2
    """
    if dose_mj_cm2 <= 0.0:
        raise ValueError("Dose-to-size must be strictly positive.")
    photon_energy_ev = calculate_euv_photon_energy_ev(wavelength_nm)
    photon_energy_j = photon_energy_ev * ELECTRON_VOLT_TO_JOULE
    energy_per_nm2_j = (dose_mj_cm2 * 1e-3) / 1e14
    return energy_per_nm2_j / photon_energy_j


def calculate_stochastic_lwr_3sigma(
    photon_density: float,
    chemical_gradient: float = 1.0
) -> float:
    """Approximate 3-sigma Line Width Roughness (nm) based on Poisson shot noise scaling.
    
    LWR_3sigma proportional to 1 / (chemical_gradient * sqrt(N_photons))
    """
    if photon_density <= 0.0:
        raise ValueError("Photon density must be strictly positive.")
    if chemical_gradient <= 0.0:
        raise ValueError("Chemical contrast gradient must be strictly positive.")
    return float(3.80 / (chemical_gradient * math.sqrt(photon_density)))


def calculate_lpp_conversion_efficiency(
    in_band_euv_power_w: float,
    driving_laser_power_w: float
) -> float:
    """Calculate laser-produced plasma (LPP) EUV in-band conversion efficiency CE."""
    if driving_laser_power_w <= 0.0:
        raise ValueError("Driving laser power must be strictly positive.")
    if in_band_euv_power_w < 0.0:
        raise ValueError("In-band EUV power cannot be negative.")
    return in_band_euv_power_w / driving_laser_power_w


def validate_euv_lithography_parameters(
    na: float,
    k1_factor: float,
    lwr_3sigma_nm: float,
    ler_3sigma_nm: float,
    dose_to_size_mj_cm2: float,
    overlay_error_nm: float,
    cdu_3sigma_nm: float,
    pellicle_transmission: float,
    tin_droplet_freq_khz: float,
    laser_power_kw: float
) -> EUVLithographyValidationResult:
    """Audit lithographic parameters against Dr. Nadia Vance's High-NA EUV invariants."""
    violations: List[str] = []
    remediation_notes: List[str] = []
    deductions: float = 0.0

    params: Dict[str, float] = {
        "na": na,
        "k1_factor": k1_factor,
        "lwr_3sigma_nm": lwr_3sigma_nm,
        "ler_3sigma_nm": ler_3sigma_nm,
        "dose_to_size_mj_cm2": dose_to_size_mj_cm2,
        "overlay_error_nm": overlay_error_nm,
        "cdu_3sigma_nm": cdu_3sigma_nm,
        "pellicle_transmission": pellicle_transmission,
        "tin_droplet_freq_khz": tin_droplet_freq_khz,
        "laser_power_kw": laser_power_kw,
    }

    # 1. High-NA Optics
    if na < MIN_HIGH_NA:
        violations.append(
            f"Numerical Aperture {na:.2f} < {MIN_HIGH_NA:.2f}: Fails High-NA EUV benchmark."
        )
        remediation_notes.append("Adopt 0.55 NA anamorphic projection optics.")
        deductions += 20.0

    # 2. Process Difficulty & Rayleigh Half-Pitch
    rayleigh_hp = calculate_rayleigh_resolution(EUV_WAVELENGTH_NM, na, k1_factor)
    if rayleigh_hp > MAX_RAYLEIGH_HALF_PITCH_NM:
        violations.append(
            f"Rayleigh Half-Pitch {rayleigh_hp:.2f} nm > {MAX_RAYLEIGH_HALF_PITCH_NM:.2f} nm: "
            "Cannot pattern sub-2nm foundry pitch."
        )
        remediation_notes.append("Tighten k1 factor and resolution to achieve HP <= 8.0 nm.")
        deductions += 15.0

    # 3. Line Width & Edge Roughness
    if lwr_3sigma_nm > MAX_LWR_3SIGMA_NM:
        violations.append(
            f"LWR 3-sigma {lwr_3sigma_nm:.2f} nm > {MAX_LWR_3SIGMA_NM:.2f} nm: "
            "Excessive stochastic line width roughness induces device variability."
        )
        remediation_notes.append("Enforce LWR_3sigma <= 1.20 nm via optimized acid generator contrast.")
        deductions += 15.0

    if ler_3sigma_nm > MAX_LER_3SIGMA_NM:
        violations.append(
            f"LER 3-sigma {ler_3sigma_nm:.2f} nm > {MAX_LER_3SIGMA_NM:.2f} nm: Line edge roughness breaches threshold."
        )
        remediation_notes.append("Enforce LER_3sigma <= 0.85 nm.")
        deductions += 10.0

    # 4. Dose-to-size & Photon Shot Noise
    if dose_to_size_mj_cm2 < MIN_DOSE_TO_SIZE_MJ_CM2:
        violations.append(
            f"Dose-to-size {dose_to_size_mj_cm2:.1f} mJ/cm^2 < {MIN_DOSE_TO_SIZE_MJ_CM2:.1f} mJ/cm^2: "
            "Insufficient photon flux enters stochastic yield cliff (microbridges/nano-pinches)."
        )
        remediation_notes.append("Elevate exposure dose >= 30.0 mJ/cm^2.")
        deductions += 15.0
    elif dose_to_size_mj_cm2 > MAX_DOSE_TO_SIZE_MJ_CM2:
        violations.append(
            f"Dose-to-size {dose_to_size_mj_cm2:.1f} mJ/cm^2 > {MAX_DOSE_TO_SIZE_MJ_CM2:.1f} mJ/cm^2: "
            "Excessive dose cripples scanner throughput below 150 wafers/hour."
        )
        remediation_notes.append("Optimize resist quantum yield to bound dose <= 75.0 mJ/cm^2.")
        deductions += 10.0

    # 5. Overlay Registration Error
    if overlay_error_nm > MAX_OVERLAY_ERROR_NM:
        violations.append(
            f"Overlay Error {overlay_error_nm:.2f} nm > {MAX_OVERLAY_ERROR_NM:.2f} nm: "
            "Layer-to-layer misalignment causes catastrophic interconnect shorts."
        )
        remediation_notes.append("Enforce dedicated chuck overlay Delta_overlay <= 1.10 nm.")
        deductions += 20.0

    # 6. Critical Dimension Uniformity (CDU)
    if cdu_3sigma_nm > MAX_CDU_3SIGMA_NM:
        violations.append(
            f"Wafer CDU 3-sigma {cdu_3sigma_nm:.2f} nm > {MAX_CDU_3SIGMA_NM:.2f} nm: "
            "Intra-field critical dimension variability exceeds node limits."
        )
        remediation_notes.append("Calibrate scanner dose uniformity to achieve CDU_3sigma <= 0.60 nm.")
        deductions += 15.0

    # 7. Pellicle EUV Transmission
    if pellicle_transmission < MIN_PELLICLE_TRANSMISSION:
        violations.append(
            f"Pellicle Transmission {pellicle_transmission * 100.0:.1f}% < {MIN_PELLICLE_TRANSMISSION * 100.0:.1f}%: "
            "Pellicle absorption degrades reticle throughput and induces thermal distortion."
        )
        remediation_notes.append("Deploy ultra-thin carbon nanotube pellicle with transmission >= 90%.")
        deductions += 10.0

    # 8. LPP Source Tin Droplet & Laser Power
    if tin_droplet_freq_khz < MIN_TIN_DROPLET_FREQ_KHZ:
        violations.append(
            f"Tin Droplet Frequency {tin_droplet_freq_khz:.1f} kHz < {MIN_TIN_DROPLET_FREQ_KHZ:.1f} kHz: "
            "Unstable plasma repetition rate."
        )
        remediation_notes.append("Maintain tin droplet generator frequency >= 50.0 kHz.")
        deductions += 10.0

    if laser_power_kw < MIN_LASER_POWER_KW:
        violations.append(
            f"Laser Drive Power {laser_power_kw:.1f} kW < {MIN_LASER_POWER_KW:.1f} kW: "
            "Insufficient drive power to sustain >500W in-band intermediate focus EUV power."
        )
        remediation_notes.append("Enforce pulsed CO2 laser drive power >= 30.0 kW.")
        deductions += 15.0

    score = max(0.0, 100.0 - deductions)
    is_valid = (score >= 95.0) and (len(violations) == 0)

    return EUVLithographyValidationResult(
        is_valid=is_valid,
        score=score,
        violations=violations,
        parameters=params,
        remediation_notes=remediation_notes
    )
