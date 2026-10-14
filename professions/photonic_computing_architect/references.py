#!/usr/bin/env python3
"""
Photonic Computing & Neuromorphic Optical References
Domain Invariants: MZI unitary decomposition, thermo-optic phase drift, WDM crosstalk, shot noise.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple

# Physical Constants
SPEED_OF_LIGHT = 299792458.0  # m/s
ELEMENTARY_CHARGE = 1.602176634e-19  # Coulombs
PLANCK_CONSTANT = 6.62607015e-34  # J*s

# Silicon Photonics Material Properties at 1550 nm
SI_GROUP_INDEX = 4.2  # Typical Si strip waveguide group index
SI_THERMO_OPTIC_COEFF = 1.86e-4  # dn/dT in 1/K


@dataclass
class PhotonicValidationResult:
    is_valid: bool
    unitary_error: float
    extinction_ratio_db: float
    phase_drift_rad: float
    wdm_crosstalk_db: float
    mac_latency_ps: float
    energy_per_mac_fj: float
    osnr_db: float
    violations: List[str] = field(default_factory=list)


def mzi_transfer_matrix(theta: float, phi: float) -> Tuple[Tuple[complex, complex], Tuple[complex, complex]]:
    """
    Computes the 2x2 complex unitary transfer matrix of a balanced Mach-Zehnder Interferometer
    with internal phase shifter theta and external phase shifter phi:
    T(theta, phi) = i * exp(i * theta / 2) * [
        [ exp(i * phi) * sin(theta / 2), exp(i * phi) * cos(theta / 2) ],
        [ cos(theta / 2), -sin(theta / 2) ]
    ]
    """
    sin_t = math.sin(theta / 2.0)
    cos_t = math.cos(theta / 2.0)
    exp_i_phi = complex(math.cos(phi), math.sin(phi))
    
    # Global phase factor i * exp(i * theta / 2)
    phase_factor = 1j * complex(math.cos(theta / 2.0), math.sin(theta / 2.0))
    
    m00 = phase_factor * exp_i_phi * sin_t
    m01 = phase_factor * exp_i_phi * cos_t
    m10 = phase_factor * cos_t
    m11 = phase_factor * (-sin_t)
    
    return ((m00, m01), (m10, m11))


def unitary_error_norm(matrix_2x2: Tuple[Tuple[complex, complex], Tuple[complex, complex]]) -> float:
    """
    Calculates the Frobenius norm of U^dagger * U - I:
    || U^dagger * U - I ||_F
    """
    ((u00, u01), (u10, u11)) = matrix_2x2
    
    # U^dagger = conjugate transpose
    ud00 = u00.conjugate()
    ud01 = u10.conjugate()
    ud10 = u01.conjugate()
    ud11 = u11.conjugate()
    
    # Product P = U^dagger * U
    p00 = ud00 * u00 + ud01 * u10
    p01 = ud00 * u01 + ud01 * u11
    p10 = ud10 * u00 + ud11 * u10
    p11 = ud10 * u01 + ud11 * u11
    
    # Diff D = P - I
    d00 = p00 - 1.0
    d01 = p01
    d10 = p10
    d11 = p11 - 1.0
    
    frob_sq = (abs(d00)**2 + abs(d01)**2 + abs(d10)**2 + abs(d11)**2)
    return math.sqrt(frob_sq)


def thermo_optic_phase_shift(
    dn_dT: float,
    delta_T_kelvin: float,
    length_m: float,
    wavelength_m: float = 1.55e-6
) -> float:
    """
    Computes thermo-optic phase shift delta_phi = (2 * pi / lambda) * (dn/dT) * delta_T * L
    """
    if wavelength_m <= 0:
        raise ValueError("Wavelength must be strictly positive.")
    return (2.0 * math.pi / wavelength_m) * dn_dT * delta_T_kelvin * length_m


def optical_mac_latency(waveguide_length_m: float, group_index: float = SI_GROUP_INDEX) -> float:
    """
    Computes light transit time through waveguide:
    tau = (n_g * L) / c in picoseconds (1 ps = 1e-12 s)
    """
    if waveguide_length_m < 0 or group_index <= 0:
        raise ValueError("Waveguide length and group index must be positive.")
    transit_seconds = (group_index * waveguide_length_m) / SPEED_OF_LIGHT
    return transit_seconds * 1.0e12  # picoseconds


def photodiode_shot_noise_current(
    responsivity_a_w: float,
    optical_power_w: float,
    bandwidth_hz: float
) -> float:
    """
    Calculates root-mean-square (RMS) shot-noise photocurrent:
    i_shot = sqrt(2 * q * I_photo * B) where I_photo = R * P_opt
    """
    if optical_power_w < 0 or bandwidth_hz <= 0 or responsivity_a_w <= 0:
        raise ValueError("Physical parameters must be strictly positive.")
    i_photo = responsivity_a_w * optical_power_w
    return math.sqrt(2.0 * ELEMENTARY_CHARGE * i_photo * bandwidth_hz)


def optical_snr_db(signal_power_w: float, noise_power_w: float) -> float:
    """
    Calculates optical signal-to-noise ratio in decibels:
    OSNR_dB = 10 * log10(P_signal / P_noise)
    """
    if signal_power_w <= 0 or noise_power_w <= 0:
        raise ValueError("Signal and noise power must be strictly positive.")
    return 10.0 * math.log10(signal_power_w / noise_power_w)


def validate_photonic_mesh(
    unitary_error: float,
    extinction_ratio_db: float,
    residual_phase_drift_rad: float,
    wdm_crosstalk_db: float,
    mac_latency_ps: float,
    energy_per_mac_fj: float,
    osnr_db: float
) -> PhotonicValidationResult:
    """
    Validates a photonic neuromorphic compute core against all physical
    and computational bounds.
    """
    violations = []
    
    # 1. Unitary error norm (<= 1.0e-4)
    if unitary_error > 1.0e-4:
        violations.append(
            f"Unitary error norm {unitary_error:.2e} > 1.0e-4 threshold; matrix non-unitarity."
        )
        
    # 2. MZI Extinction Ratio (>= 25.0 dB)
    if extinction_ratio_db < 25.0:
        violations.append(
            f"MZI extinction ratio {extinction_ratio_db:.1f} dB < 25.0 dB minimum contrast."
        )
        
    # 3. Residual thermal phase drift (<= 0.01 rad)
    if residual_phase_drift_rad > 0.01:
        violations.append(
            f"Residual thermal phase drift {residual_phase_drift_rad:.4f} rad > 0.01 rad bound."
        )
        
    # 4. WDM Channel Crosstalk (<= -25.0 dB)
    if wdm_crosstalk_db > -25.0:
        violations.append(
            f"WDM inter-channel crosstalk {wdm_crosstalk_db:.1f} dB > -25.0 dB isolation limit."
        )
        
    # 5. Energy consumption (<= 10.0 fJ/MAC)
    if energy_per_mac_fj > 10.0:
        violations.append(
            f"Energy per MAC {energy_per_mac_fj:.2f} fJ > 10.0 fJ limit; thermal overrun."
        )
        
    # 6. Optical SNR (>= 30.0 dB)
    if osnr_db < 30.0:
        violations.append(
            f"Optical SNR {osnr_db:.1f} dB < 30.0 dB minimum precision limit."
        )
        
    is_valid = (len(violations) == 0)
    return PhotonicValidationResult(
        is_valid=is_valid,
        unitary_error=unitary_error,
        extinction_ratio_db=extinction_ratio_db,
        phase_drift_rad=residual_phase_drift_rad,
        wdm_crosstalk_db=wdm_crosstalk_db,
        mac_latency_ps=mac_latency_ps,
        energy_per_mac_fj=energy_per_mac_fj,
        osnr_db=osnr_db,
        violations=violations
    )
