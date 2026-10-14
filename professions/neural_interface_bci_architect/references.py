#!/usr/bin/env python3
"""
Neural Interface & Biomechatronic BCI References
Domain Invariants: Shannon charge injection safety limits, Pennes bioheat tissue thermal rise,
electrode-tissue interface Randles impedance, active biphasic charge balancing,
and sub-10ms closed-loop neural decoding latency.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class NeuralInterfaceValidationResult:
    is_valid: bool
    shannon_k: float
    tissue_temp_rise_c: float
    decoding_latency_ms: float
    electrode_impedance_kohm: float
    front_end_cmrr_db: float
    residual_charge_pc: float
    violations: List[str] = field(default_factory=list)


def shannon_safety_limit(charge_per_phase_uc: float, geometric_area_cm2: float) -> float:
    """
    Computes the Shannon electrochemical safety index k:
    log10(Q / A) = k - log10(Q)  =>  k = log10(Q / A) + log10(Q)
    where Q is charge per phase in uC and A is geometric surface area in cm^2.
    Safe boundary: k <= 1.75 (prevents neural damage and electrode corrosion).
    """
    if charge_per_phase_uc <= 0 or geometric_area_cm2 <= 0:
        raise ValueError("Charge per phase and electrode area must be strictly positive.")
    charge_density = charge_per_phase_uc / geometric_area_cm2
    return math.log10(charge_density) + math.log10(charge_per_phase_uc)


def tissue_temperature_rise(power_dissipated_mw: float, surface_area_cm2: float) -> float:
    """
    Estimates steady-state cortical tissue temperature rise (deg C) based on heat flux:
    Delta_T = (P_diss / Area) / h_eff
    where h_eff approx 40.0 mW / (cm^2 * deg C) for cortical micro-circulation.
    """
    if power_dissipated_mw < 0 or surface_area_cm2 <= 0:
        raise ValueError("Power must be non-negative and surface area strictly positive.")
    p_density = power_dissipated_mw / surface_area_cm2
    h_eff = 40.0  # mW / (cm^2 * deg C)
    return p_density / h_eff


def electrode_interface_impedance(r_solution_ohms: float, c_double_layer_f: float, freq_hz: float = 1000.0) -> float:
    """
    Calculates Randles equivalent circuit impedance magnitude |Z| of neural electrode:
    |Z| = sqrt(R_s^2 + (1 / (2 * pi * f * C_dl))^2) in Ohms.
    """
    if r_solution_ohms < 0 or c_double_layer_f <= 0 or freq_hz <= 0:
        raise ValueError("Parameters must be non-negative with positive capacitance and frequency.")
    x_c = 1.0 / (2.0 * math.pi * freq_hz * c_double_layer_f)
    return math.sqrt(r_solution_ohms**2 + x_c**2)


def biphasic_charge_balance_error(q_cathodic_pc: float, q_anodic_pc: float) -> float:
    """
    Calculates residual charge imbalance per biphasic pulse:
    Delta_Q = |Q_cathodic - Q_anodic| (picoCoulombs).
    """
    if q_cathodic_pc < 0 or q_anodic_pc < 0:
        raise ValueError("Charges must be non-negative magnitudes.")
    return abs(q_cathodic_pc - q_anodic_pc)


def decoding_latency_budget(
    t_spike_detect_ms: float,
    t_feature_extract_ms: float,
    t_model_infer_ms: float,
    t_actuator_comm_ms: float
) -> float:
    """
    Calculates total closed-loop BCI loop latency:
    tau = t_spike + t_feature + t_infer + t_actuator.
    """
    if any(t < 0 for t in [t_spike_detect_ms, t_feature_extract_ms, t_model_infer_ms, t_actuator_comm_ms]):
        raise ValueError("Latency component values cannot be negative.")
    return t_spike_detect_ms + t_feature_extract_ms + t_model_infer_ms + t_actuator_comm_ms


def validate_neural_interface(
    shannon_k: float,
    tissue_temp_rise_c: float,
    decoding_latency_ms: float,
    electrode_impedance_kohm: float,
    front_end_cmrr_db: float,
    residual_charge_pc: float
) -> NeuralInterfaceValidationResult:
    """
    Validates a neural interface and BCI neuroprosthetic system against
    electrochemical, thermal, and sensorimotor timing limits.
    """
    violations = []

    # 1. Shannon Safety Index (<= 1.75)
    if shannon_k > 1.75:
        violations.append(
            f"Shannon safety index k={shannon_k:.2f} > 1.75 limit; causes irreversible tissue damage and electrode dissolution."
        )

    # 2. Cortical Tissue Heating (<= 1.0 deg C)
    if tissue_temp_rise_c > 1.0:
        violations.append(
            f"Cortical tissue temperature rise {tissue_temp_rise_c:.2f} C > 1.0 C limit; parenchymal thermal necrosis risk."
        )

    # 3. Closed-Loop Decoding Latency (<= 10.0 ms)
    if decoding_latency_ms > 10.0:
        violations.append(
            f"Decoding loop latency {decoding_latency_ms:.1f} ms > 10.0 ms limit; neuroprosthetic ataxia and sensorimotor lag."
        )

    # 4. Electrode Impedance at 1 kHz (<= 500.0 kohm)
    if electrode_impedance_kohm > 500.0:
        violations.append(
            f"Electrode impedance {electrode_impedance_kohm:.1f} kohm > 500.0 kohm; glial scar encapsulation and SNR collapse."
        )

    # 5. Front-End CMRR (>= 90.0 dB)
    if front_end_cmrr_db < 90.0:
        violations.append(
            f"Common-Mode Rejection {front_end_cmrr_db:.1f} dB < 90.0 dB threshold; contamination by 50/60Hz and EMG motion artifacts."
        )

    # 6. Residual Biphasic Charge (<= 1.0 pC)
    if residual_charge_pc > 1.0:
        violations.append(
            f"Residual pulse charge {residual_charge_pc:.2f} pC > 1.0 pC limit; electrolytic pH shift and tissue electrolysis."
        )

    is_valid = (len(violations) == 0)
    return NeuralInterfaceValidationResult(
        is_valid=is_valid,
        shannon_k=shannon_k,
        tissue_temp_rise_c=tissue_temp_rise_c,
        decoding_latency_ms=decoding_latency_ms,
        electrode_impedance_kohm=electrode_impedance_kohm,
        front_end_cmrr_db=front_end_cmrr_db,
        residual_charge_pc=residual_charge_pc,
        violations=violations
    )
