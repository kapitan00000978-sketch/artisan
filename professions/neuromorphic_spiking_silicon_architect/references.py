#!/usr/bin/env python3
"""
Neuromorphic Spiking Silicon Mathematical References
Domain Invariants: Leaky Integrate-and-Fire (LIF), STDP plasticity, AER asynchronous encoding, energy limits.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple


@dataclass
class NeuromorphicValidationResult:
    is_valid: bool
    refractory_period_ms: float
    stdp_ratio: float
    aer_packet_loss: float
    energy_per_synop_pj: float
    mean_firing_rate_hz: float
    violations: List[str] = field(default_factory=list)


def lif_step(
    v_mem: float,
    i_syn: float,
    dt_ms: float,
    tau_m_ms: float = 20.0,
    v_rest_mv: float = -70.0,
    v_reset_mv: float = -65.0,
    v_thresh_mv: float = -50.0,
    refractory_time_left_ms: float = 0.0,
    tau_ref_ms: float = 2.0
) -> Tuple[float, bool, float]:
    """
    Computes a single discrete time-step update for a Leaky Integrate-and-Fire (LIF) neuron.
    Returns (v_next_mv, spiked, new_refractory_time_left_ms).
    """
    if dt_ms <= 0 or tau_m_ms <= 0:
        raise ValueError("Time step dt and tau_m must be strictly positive.")
    if not (v_rest_mv <= v_reset_mv < v_thresh_mv):
        raise ValueError("Voltages must satisfy v_rest <= v_reset < v_thresh.")
    
    # Check if in refractory period
    if refractory_time_left_ms > 0.0:
        new_ref = max(0.0, refractory_time_left_ms - dt_ms)
        return v_reset_mv, False, new_ref

    # Leaky integration dV/dt = (-(V - V_rest) + I_syn) / tau_m
    dv = (-(v_mem - v_rest_mv) + i_syn) * (dt_ms / tau_m_ms)
    v_tentative = v_mem + dv

    # Threshold comparison
    if v_tentative >= v_thresh_mv:
        # Emit spike and enter refractory period
        return v_reset_mv, True, tau_ref_ms
    else:
        return v_tentative, False, 0.0


def stdp_weight_update(
    w_current: float,
    delta_t_ms: float,
    a_plus: float = 0.01,
    a_minus: float = 0.012,
    tau_plus_ms: float = 20.0,
    tau_minus_ms: float = 20.0,
    w_min: float = 0.0,
    w_max: float = 1.0
) -> float:
    """
    Calculates asymmetric Spike-Timing-Dependent Plasticity (STDP) weight update:
    delta_t = t_post - t_pre
    If delta_t > 0: LTP: dw = A+ * exp(-delta_t / tau+)
    If delta_t < 0: LTD: dw = -A- * exp(delta_t / tau-)
    Weights are strictly clipped to [w_min, w_max].
    """
    if a_plus <= 0 or a_minus <= 0 or tau_plus_ms <= 0 or tau_minus_ms <= 0:
        raise ValueError("STDP learning rates and time constants must be strictly positive.")
    if w_min >= w_max:
        raise ValueError("w_min must be strictly less than w_max.")
    
    if delta_t_ms > 0:
        dw = a_plus * math.exp(-delta_t_ms / tau_plus_ms)
    elif delta_t_ms < 0:
        dw = -a_minus * math.exp(delta_t_ms / tau_minus_ms)
    else:
        dw = 0.0

    updated_w = w_current + dw
    return max(w_min, min(w_max, updated_w))


def aer_packet_encode(core_id: int, neuron_id: int, timestamp_us: int) -> int:
    """
    Encodes asynchronous spike event into a 64-bit Address-Event Representation (AER) packet:
    [Bits 63..48: core_id (16b)] [Bits 47..32: neuron_id (16b)] [Bits 31..0: timestamp_us (32b)]
    """
    if not (0 <= core_id < 65536 and 0 <= neuron_id < 65536):
        raise ValueError("Core and neuron IDs must fit in 16-bit fields.")
    if timestamp_us < 0 or timestamp_us >= (1 << 32):
        raise ValueError("Timestamp must fit in 32-bit unsigned field.")
    return (core_id << 48) | (neuron_id << 32) | timestamp_us


def aer_packet_decode(packet_64bit: int) -> Tuple[int, int, int]:
    """
    Decodes 64-bit AER packet into (core_id, neuron_id, timestamp_us).
    """
    core_id = (packet_64bit >> 48) & 0xFFFF
    neuron_id = (packet_64bit >> 32) & 0xFFFF
    timestamp_us = packet_64bit & 0xFFFFFFFF
    return core_id, neuron_id, timestamp_us


def synaptic_energy_pj(current_amps: float, voltage_volts: float, pulse_duration_s: float) -> float:
    """
    Calculates energy consumed per synaptic operation in picojoules (1 pJ = 1e-12 J):
    E = V * I * t * 1e12
    """
    if current_amps < 0 or voltage_volts < 0 or pulse_duration_s < 0:
        raise ValueError("Physical parameters must be non-negative.")
    joules = voltage_volts * current_amps * pulse_duration_s
    return joules * 1.0e12  # picojoules


def validate_neuromorphic_core(
    refractory_period_ms: float,
    stdp_a_minus: float,
    stdp_a_plus: float,
    aer_packet_loss_rate: float,
    energy_per_synop_pj: float,
    mean_firing_rate_hz: float
) -> NeuromorphicValidationResult:
    """
    Validates a neuromorphic spiking compute core against biological realism
    and physical silicon bounds.
    """
    violations = []
    
    # 1. Refractory period (>= 1.0 ms)
    if refractory_period_ms < 1.0:
        violations.append(
            f"Refractory period {refractory_period_ms:.2f} ms < 1.0 ms bound; risks infinite spiking loop."
        )
        
    # 2. STDP ratio A_minus / A_plus (>= 1.05)
    if stdp_a_plus <= 0:
        ratio = 0.0
        violations.append("STDP A_plus must be strictly positive.")
    else:
        ratio = stdp_a_minus / stdp_a_plus
        if ratio < 1.05:
            violations.append(
                f"STDP depression/potentiation ratio {ratio:.3f} < 1.05; runaway weight explosion risk."
            )
            
    # 3. AER packet loss rate (<= 1.0e-6)
    if aer_packet_loss_rate > 1.0e-6:
        violations.append(
            f"AER packet loss rate {aer_packet_loss_rate:.2e} > 1.0e-6 limit; temporal spike loss."
        )
        
    # 4. Energy per synaptic operation (<= 1.0 pJ)
    if energy_per_synop_pj > 1.0:
        violations.append(
            f"Synaptic energy {energy_per_synop_pj:.3f} pJ > 1.0 pJ bound; thermal overload."
        )
        
    # 5. Mean firing rate (0.1 - 20.0 Hz)
    if not (0.1 <= mean_firing_rate_hz <= 20.0):
        violations.append(
            f"Mean firing rate {mean_firing_rate_hz:.2f} Hz outside sparse [0.1, 20.0] Hz window."
        )
        
    is_valid = (len(violations) == 0)
    return NeuromorphicValidationResult(
        is_valid=is_valid,
        refractory_period_ms=refractory_period_ms,
        stdp_ratio=ratio,
        aer_packet_loss=aer_packet_loss_rate,
        energy_per_synop_pj=energy_per_synop_pj,
        mean_firing_rate_hz=mean_firing_rate_hz,
        violations=violations
    )
