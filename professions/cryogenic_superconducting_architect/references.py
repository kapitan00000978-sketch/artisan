#!/usr/bin/env python3
"""
Cryogenic Superconducting & Dilution Refrigerator References
Domain Invariants: 3He/4He dilution cooling power, Kapitza thermal boundary resistance,
superconducting critical current surface, Stefan-Boltzmann radiation shielding.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List

# Physical Constants
STEFAN_BOLTZMANN = 5.670374419e-8  # W / (m^2 * K^4)
DILUTION_COOLING_COEFF = 84.0  # J / (mol * K^2) for 3He/4He dilution


@dataclass
class CryogenicValidationResult:
    is_valid: bool
    cooling_power_uw: float
    base_temp_mk: float
    superconducting_margin_sf: float
    parasitic_heat_leak_uw: float
    vibration_amplitude_g: float
    insulation_vacuum_mbar: float
    violations: List[str] = field(default_factory=list)


def dilution_cooling_power_w(n_dot_3_mol_s: float, t_mix_k: float) -> float:
    """
    Calculates the theoretical cooling power of a 3He/4He dilution refrigerator:
    Q_dot = 84 * n_dot_3 * T_mix^2 (Watts)
    where n_dot_3 is in mol/s and T_mix is in Kelvin.
    """
    if n_dot_3_mol_s <= 0:
        raise ValueError("3He circulation molar rate must be strictly positive.")
    if t_mix_k <= 0:
        raise ValueError("Mixing chamber temperature must be strictly positive.")
    return DILUTION_COOLING_COEFF * n_dot_3_mol_s * (t_mix_k ** 2)


def kapitza_temperature_drop(
    heat_flow_w: float,
    area_m2: float,
    t_boundary_k: float,
    kapitza_coeff: float = 2.0e-3
) -> float:
    """
    Calculates thermal boundary temperature jump using acoustic Kapitza resistance:
    Delta_T = (R_K * Q_dot) / A where R_K = kapitza_coeff / T^3 (K)
    """
    if area_m2 <= 0 or t_boundary_k <= 0:
        raise ValueError("Area and temperature must be strictly positive.")
    if heat_flow_w < 0:
        raise ValueError("Heat flow must be non-negative.")
    r_kapitza = kapitza_coeff / (t_boundary_k ** 3)
    return (r_kapitza * heat_flow_w) / area_m2


def superconducting_critical_current(
    ic_0: float,
    t_k: float,
    tc_k: float,
    b_tesla: float,
    bc2_tesla: float
) -> float:
    """
    Computes critical current from empirical parabolic critical surface:
    Ic(T, B) = Ic0 * max(0, 1 - (T/Tc)^2) * max(0, 1 - B/Bc2)
    """
    if ic_0 <= 0 or tc_k <= 0 or bc2_tesla <= 0:
        raise ValueError("Zero-field parameters and critical thresholds must be positive.")
    if t_k >= tc_k or b_tesla >= bc2_tesla:
        return 0.0
    
    t_factor = 1.0 - (t_k / tc_k) ** 2
    b_factor = 1.0 - (b_tesla / bc2_tesla)
    return ic_0 * max(0.0, t_factor) * max(0.0, b_factor)


def thermal_radiation_heat_leak_w(
    area_m2: float,
    t_hot_k: float,
    t_cold_k: float,
    emissivity_eff: float = 0.03
) -> float:
    """
    Computes radiative heat leak between stages via Stefan-Boltzmann law with MLI shielding:
    Q_rad = sigma * A * eps_eff * (T_hot^4 - T_cold^4)
    """
    if area_m2 <= 0 or t_hot_k < t_cold_k or t_cold_k < 0:
        raise ValueError("Unphysical temperature or geometric boundary.")
    if not (0.0 < emissivity_eff <= 1.0):
        raise ValueError("Effective emissivity must be in (0, 1].")
    return STEFAN_BOLTZMANN * area_m2 * emissivity_eff * (t_hot_k**4 - t_cold_k**4)


def microphonic_detuning_hz(acceleration_g: float, compliance_hz_per_g: float = 120.0) -> float:
    """
    Computes microphonic frequency jitter in superconducting qubit/cavity:
    Delta_f = a * df/da
    """
    if acceleration_g < 0:
        raise ValueError("Acceleration magnitude must be non-negative.")
    return acceleration_g * compliance_hz_per_g


def validate_cryogenic_fridge(
    base_temp_mk: float,
    operating_current_a: float,
    critical_current_a: float,
    parasitic_heat_leak_uw: float,
    vibration_amplitude_g: float,
    insulation_vacuum_mbar: float,
    n_dot_3_mol_s: float = 1.0e-4
) -> CryogenicValidationResult:
    """
    Validates a dilution refrigerator and superconducting quantum payload against
    cryogenic thermal and electromagnetic limits.
    """
    violations = []
    
    # 1. Base temperature (<= 15.0 mK)
    if base_temp_mk > 15.0:
        violations.append(
            f"Base temperature {base_temp_mk:.1f} mK > 15.0 mK limit; causes severe thermal dephasing."
        )
        
    # 2. Superconducting margin safety factor (>= 1.30)
    if operating_current_a <= 0:
        sf = 0.0
        violations.append("Operating current must be strictly positive.")
    else:
        sf = critical_current_a / operating_current_a
        if sf < 1.30:
            violations.append(
                f"Superconducting safety factor {sf:.2f} < 1.30 minimum margin; quench danger."
            )
            
    # 3. Parasitic heat leak (<= 1.0 uW at mixing chamber)
    if parasitic_heat_leak_uw > 1.0:
        violations.append(
            f"Parasitic heat leak {parasitic_heat_leak_uw:.2f} uW > 1.0 uW budget."
        )
        
    # 4. Mechanical vibration amplitude (<= 1.0e-4 g)
    if vibration_amplitude_g > 1.0e-4:
        violations.append(
            f"Vibration acceleration {vibration_amplitude_g:.2e} g > 1.0e-4 g threshold; microphonics."
        )
        
    # 5. Insulation vacuum (<= 1.0e-6 mbar)
    if insulation_vacuum_mbar > 1.0e-6:
        violations.append(
            f"Insulation vacuum {insulation_vacuum_mbar:.2e} mbar > 1.0e-6 mbar; gas conduction short."
        )
        
    t_mix_k = base_temp_mk * 1.0e-3
    cooling_power_uw = dilution_cooling_power_w(n_dot_3_mol_s, t_mix_k) * 1.0e6

    is_valid = (len(violations) == 0)
    return CryogenicValidationResult(
        is_valid=is_valid,
        cooling_power_uw=cooling_power_uw,
        base_temp_mk=base_temp_mk,
        superconducting_margin_sf=sf,
        parasitic_heat_leak_uw=parasitic_heat_leak_uw,
        vibration_amplitude_g=vibration_amplitude_g,
        insulation_vacuum_mbar=insulation_vacuum_mbar,
        violations=violations
    )
