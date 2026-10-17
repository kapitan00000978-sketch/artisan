"""Physical references and mathematical models for Optical Lattice Atomic Clocks & Quantum Metrology.

Architect: Dr. Eliana 'The Chrono-Metrology' Sterling
Domain: optical_lattice_clock_metrology_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Fundamental physical constants
SPEED_OF_LIGHT: float = 299792458.0                # m/s
PLANCK_CONSTANT: float = 6.62607015e-34            # J*s
REDUCED_PLANCK: float = 1.054571817e-34            # J*s
BOLTZMANN_CONSTANT: float = 1.380649e-23           # J/K
STANDARD_GRAVITY: float = 9.80665                  # m/s^2

# Atomic reference standards for Strontium-87 (^87Sr, 1S0 -> 3P0 clock transition)
SR87_CLOCK_TRANSITION_FREQ_HZ: float = 429228004229873.0  # ~429.228 THz
SR87_CLOCK_TRANSITION_WAVELENGTH_NM: float = 698.446       # nm
SR87_MAGIC_WAVELENGTH_NM: float = 813.428                  # nm
YB171_MAGIC_WAVELENGTH_NM: float = 759.355                 # nm

# Quantitative engineering benchmarks for state-of-the-art optical lattice clocks
MAX_FRACTIONAL_INACCURACY: float = 1.0e-18         # Delta_nu / nu_0 <= 1.0e-18
MAX_ALLAN_DEV_COEFF: float = 1.0e-16               # sigma_y(tau) <= 1.0e-16 / sqrt(tau)
MAX_MAGIC_WAVELENGTH_DETUNING_NM: float = 0.05     # |lambda_lattice - lambda_magic| <= 0.05 nm
MAX_LASER_LINEWIDTH_MHZ: float = 10.0              # Delta_nu_laser <= 10.0 mHz (0.010 Hz)
MIN_CAVITY_FINESSE: float = 500000.0               # F >= 500,000
MIN_SILICON_CAVITY_TEMP_K: float = 123.0           # Silicon alpha(T) = 0 crossing [123, 125] K
MAX_SILICON_CAVITY_TEMP_K: float = 125.0
MAX_BBR_TEMP_UNCERTAINTY_MK: float = 10.0          # Delta T_env <= 10.0 mK
MAX_ATOM_TEMPERATURE_UK: float = 2.0               # T_atom <= 2.0 microkelvin
MAX_COLLISIONAL_SHIFT_FRACTION: float = 1.0e-19    # |Delta_nu_coll / nu_0| <= 1.0e-19
MAX_RESIDUAL_ZEEMAN_UT: float = 1.0                # B_res <= 1.0 microtesla


def calculate_gravitational_redshift_fraction(
    height_difference_m: float,
    local_gravity: float = STANDARD_GRAVITY
) -> float:
    """Calculate the relativistic gravitational redshift fractional frequency shift.

    Delta_nu / nu_0 = (g * Delta_h) / c^2
    ~1.09e-16 per meter of elevation (1.09e-18 per centimeter)
    """
    return (local_gravity * height_difference_m) / (SPEED_OF_LIGHT ** 2)


def calculate_allan_deviation(
    instability_coeff: float,
    tau_seconds: float
) -> float:
    """Calculate white frequency noise Allan deviation at averaging time tau in seconds.

    sigma_y(tau) = instability_coeff / sqrt(tau)
    """
    if tau_seconds <= 0.0:
        return float("inf")
    return instability_coeff / math.sqrt(tau_seconds)


def calculate_ac_stark_shift_fraction(
    lattice_wavelength_nm: float,
    magic_wavelength_nm: float,
    trap_depth_microkelvin: float = 20.0
) -> float:
    """Calculate residual differential AC Stark shift fraction due to magic wavelength detuning.

    Delta_nu_Stark / nu_0 ~ C_stark * (lambda - lambda_magic) * U_0
    """
    detuning_nm = abs(lattice_wavelength_nm - magic_wavelength_nm)
    # Empirical slope for ^87Sr: ~2.5e-19 per nm of detuning per microkelvin trap depth
    c_stark = 2.5e-19
    return c_stark * detuning_nm * max(0.0, trap_depth_microkelvin)


def calculate_quantum_projection_noise_limit(
    q_factor: float,
    num_atoms: int,
    cycle_time_s: float,
    tau_s: float
) -> float:
    """Calculate quantum projection noise (QPN) limit of optical clock.

    sigma_QPN(tau) = 1 / (pi * Q * sqrt(N_atom)) * sqrt(T_cycle / tau)
    """
    if q_factor <= 0.0 or num_atoms <= 0 or tau_s <= 0.0:
        return float("inf")
    return (1.0 / (math.pi * q_factor * math.sqrt(num_atoms))) * math.sqrt(cycle_time_s / tau_s)


@dataclass
class OpticalClockValidationResult:
    """Structured validation report for Optical Lattice Atomic Clock & Quantum Metrology."""
    is_valid: bool
    fractional_inaccuracy: float
    allan_deviation_1s: float
    magic_wavelength_detuning_nm: float
    laser_linewidth_mhz: float
    cavity_finesse: float
    cavity_temperature_k: float
    bbr_temp_uncertainty_mk: float
    atom_temperature_uk: float
    collisional_shift_fraction: float
    residual_zeeman_ut: float
    flaws: List[str]


def validate_optical_clock_parameters(
    fractional_inaccuracy: float = 8.5e-19,
    allan_deviation_1s: float = 7.2e-17,
    magic_wavelength_detuning_nm: float = 0.012,
    laser_linewidth_mhz: float = 6.5,
    cavity_finesse: float = 650000.0,
    cavity_temperature_k: float = 124.0,
    bbr_temp_uncertainty_mk: float = 6.0,
    atom_temperature_uk: float = 1.2,
    collisional_shift_fraction: float = 4.5e-20,
    residual_zeeman_ut: float = 0.45
) -> OpticalClockValidationResult:
    """Validate optical lattice clock parameters against Dr. Eliana Sterling's strict metrology benchmarks."""
    flaws: List[str] = []

    if fractional_inaccuracy > MAX_FRACTIONAL_INACCURACY:
        flaws.append(
            f"Fractional frequency inaccuracy {fractional_inaccuracy:.2e} exceeds maximum allowable uncertainty "
            f"{MAX_FRACTIONAL_INACCURACY:.2e}."
        )

    if allan_deviation_1s > MAX_ALLAN_DEV_COEFF:
        flaws.append(
            f"Short-term 1-second Allan deviation {allan_deviation_1s:.2e} exceeds stability bound "
            f"{MAX_ALLAN_DEV_COEFF:.2e}."
        )

    if magic_wavelength_detuning_nm > MAX_MAGIC_WAVELENGTH_DETUNING_NM:
        flaws.append(
            f"Lattice magic wavelength detuning {magic_wavelength_detuning_nm:.4f} nm exceeds tolerance "
            f"{MAX_MAGIC_WAVELENGTH_DETUNING_NM:.3f} nm (inducing differential AC Stark shifts)."
        )

    if laser_linewidth_mhz > MAX_LASER_LINEWIDTH_MHZ:
        flaws.append(
            f"Clock interrogation laser linewidth {laser_linewidth_mhz:.2f} mHz exceeds sub-millihertz ceiling "
            f"{MAX_LASER_LINEWIDTH_MHZ:.1f} mHz."
        )

    if cavity_finesse < MIN_CAVITY_FINESSE:
        flaws.append(
            f"Reference cavity finesse {cavity_finesse:,.0f} below high-finesse threshold "
            f"{MIN_CAVITY_FINESSE:,.0f}."
        )

    if cavity_temperature_k < MIN_SILICON_CAVITY_TEMP_K or cavity_temperature_k > MAX_SILICON_CAVITY_TEMP_K:
        flaws.append(
            f"Cryogenic silicon cavity temperature {cavity_temperature_k:.2f} K outside thermal null expansion window "
            f"[{MIN_SILICON_CAVITY_TEMP_K:.1f}, {MAX_SILICON_CAVITY_TEMP_K:.1f}] K."
        )

    if bbr_temp_uncertainty_mk > MAX_BBR_TEMP_UNCERTAINTY_MK:
        flaws.append(
            f"Blackbody radiation (BBR) temperature uncertainty {bbr_temp_uncertainty_mk:.1f} mK exceeds "
            f"{MAX_BBR_TEMP_UNCERTAINTY_MK:.1f} mK."
        )

    if atom_temperature_uk > MAX_ATOM_TEMPERATURE_UK:
        flaws.append(
            f"Trapped atom temperature {atom_temperature_uk:.2f} microkelvin exceeds Lamb-Dicke limit "
            f"{MAX_ATOM_TEMPERATURE_UK:.1f} microkelvin."
        )

    if collisional_shift_fraction > MAX_COLLISIONAL_SHIFT_FRACTION:
        flaws.append(
            f"Collisional density frequency shift {collisional_shift_fraction:.2e} exceeds Pauli exclusion cap "
            f"{MAX_COLLISIONAL_SHIFT_FRACTION:.2e}."
        )

    if residual_zeeman_ut > MAX_RESIDUAL_ZEEMAN_UT:
        flaws.append(
            f"Residual uncompensated Zeeman field {residual_zeeman_ut:.2f} microtesla exceeds magnetic shielding limit "
            f"{MAX_RESIDUAL_ZEEMAN_UT:.1f} microtesla."
        )

    return OpticalClockValidationResult(
        is_valid=len(flaws) == 0,
        fractional_inaccuracy=fractional_inaccuracy,
        allan_deviation_1s=allan_deviation_1s,
        magic_wavelength_detuning_nm=magic_wavelength_detuning_nm,
        laser_linewidth_mhz=laser_linewidth_mhz,
        cavity_finesse=cavity_finesse,
        cavity_temperature_k=cavity_temperature_k,
        bbr_temp_uncertainty_mk=bbr_temp_uncertainty_mk,
        atom_temperature_uk=atom_temperature_uk,
        collisional_shift_fraction=collisional_shift_fraction,
        residual_zeeman_ut=residual_zeeman_ut,
        flaws=flaws
    )
