#!/usr/bin/env python3
"""
Unit Test Suite for Dr. Thalia 'The Synapse' Sterling
Neuromorphic Spiking Silicon & Event-Driven Systems Architect Master Subsystem
"""

import math
import pytest
from professions.neuromorphic_spiking_silicon_architect import (
    lif_step,
    stdp_weight_update,
    aer_packet_encode,
    aer_packet_decode,
    synaptic_energy_pj,
    validate_neuromorphic_core,
    NeuromorphicInspector,
    NeuromorphicRubric,
    NeuromorphicBlindCritic,
    NeuromorphicElevationEngine,
    DrThaliaSterling
)


def test_lif_integration_and_refractory_period():
    # Parameters
    v_rest = -70.0
    v_reset = -65.0
    v_thresh = -50.0
    tau_ref = 2.0
    dt = 0.5

    # 1. Subthreshold integration with small input
    v = v_rest
    v, spiked, ref = lif_step(v, i_syn=5.0, dt_ms=dt, v_rest_mv=v_rest, v_reset_mv=v_reset, v_thresh_mv=v_thresh)
    assert not spiked
    assert v > v_rest
    assert ref == 0.0

    # 2. Strong current causing spike
    v = -52.0
    v_post, spiked, ref = lif_step(v, i_syn=100.0, dt_ms=dt, v_rest_mv=v_rest, v_reset_mv=v_reset, v_thresh_mv=v_thresh, tau_ref_ms=tau_ref)
    assert spiked is True
    assert v_post == v_reset
    assert ref == tau_ref

    # 3. In refractory period: must not spike even under extreme current
    v_ref, spiked_ref, ref_left = lif_step(v_post, i_syn=1000.0, dt_ms=dt, refractory_time_left_ms=ref, tau_ref_ms=tau_ref)
    assert spiked_ref is False
    assert v_ref == v_reset
    assert math.isclose(ref_left, tau_ref - dt, abs_tol=1e-5)


def test_stdp_hebbian_plasticity_and_saturation():
    w_init = 0.5
    # 1. Pre before post (delta_t = +10 ms -> LTP potentiation)
    w_ltp = stdp_weight_update(w_init, delta_t_ms=10.0, a_plus=0.02, tau_plus_ms=20.0)
    assert w_ltp > w_init

    # 2. Post before pre (delta_t = -10 ms -> LTD depression)
    w_ltd = stdp_weight_update(w_init, delta_t_ms=-10.0, a_minus=0.025, tau_minus_ms=20.0)
    assert w_ltd < w_init

    # 3. Saturation envelope clipping [0.0, 1.0]
    w_overflow = stdp_weight_update(0.99, delta_t_ms=1.0, a_plus=0.5)
    assert w_overflow == 1.0

    w_underflow = stdp_weight_update(0.01, delta_t_ms=-1.0, a_minus=0.5)
    assert w_underflow == 0.0


def test_aer_packet_encoding_and_decoding():
    core_id = 42
    neuron_id = 1024
    timestamp_us = 987654321

    packet = aer_packet_encode(core_id, neuron_id, timestamp_us)
    dec_core, dec_neuron, dec_ts = aer_packet_decode(packet)

    assert dec_core == core_id
    assert dec_neuron == neuron_id
    assert dec_ts == timestamp_us


def test_synaptic_energy_bounds():
    # 0.8 V, 50 nA, 10 ns spike pulse
    voltage = 0.8
    current = 50.0e-9
    pulse_width = 10.0e-9

    energy_pj = synaptic_energy_pj(current, voltage, pulse_width)
    # Expected: 0.8 * 50e-9 * 10e-9 = 4e-16 J = 0.0004 pJ (400 aJ)
    assert energy_pj < 1.0  # Well within 1 pJ bound
    assert 0.0001 < energy_pj < 0.01


def test_neuromorphic_inspector_and_rubric():
    inspector = NeuromorphicInspector()

    clean_code = """
def execute_spiking_core():
    refractory_period = 2.5
    stdp_ratio = 1.15
    clip_synaptic_weights = True
    aer_packet_drop = 2.0e-7
    energy_per_synop = 0.45
    mean_firing_rate = 4.5
    return "SNN Running"
"""
    clean_flaws = inspector.inspect_code(clean_code)
    clean_eval = NeuromorphicRubric.evaluate(clean_flaws)
    assert len(clean_flaws) == 0
    assert clean_eval["passed"] is True
    assert clean_eval["score"] == 100

    flawed_code = """
def execute_spiking_core():
    refractory_period = 0.2
    stdp_ratio = 0.95
    clip_synaptic_weights = False
    aer_packet_drop = 5.0e-4
    energy_per_synop = 8.5
    mean_firing_rate = 120.0
    try:
        deliver_aer_spike()
    except Exception:
        pass
    return "Uncontrolled"
"""
    flawed_issues = inspector.inspect_code(flawed_code)
    flawed_eval = NeuromorphicRubric.evaluate(flawed_issues)
    assert len(flawed_issues) >= 6
    assert flawed_eval["passed"] is False
    assert flawed_eval["score"] < 40


def test_blind_critic_adversarial_rejection():
    critic = NeuromorphicBlindCritic()
    bursting_network = """
def cortex_simulation():
    ref_period_ms = 0.1
    stdp_ratio = 0.90
    clip_synaptic_weights = False
    return "Burst"
"""
    audit = critic.audit(bursting_network)
    assert audit["verdict"] == "REJECTED"
    assert audit["score"] < 95
    assert audit["flaw_count"] >= 3


def test_elevation_engine_and_master_closed_loop():
    flawed_script = """
def cortical_microcircuit():
    refractory_period = 0.3
    stdp_ratio = 0.92
    clip_synaptic_weights = False
    aer_packet_drop = 8.0e-5
    energy_per_synop = 4.5
    mean_firing_rate = 85.0
    try:
        route_aer_events()
    except Exception:
        pass
    return "Simulated"
"""
    master = DrThaliaSterling(min_passing_score=95)
    result = master.execute_closed_loop(flawed_script, target_file="spiking_mesh.py")

    assert result["status"] == "CERTIFIED"
    assert result["final_score"] >= 95
    assert "Thalia" in result["master"]
    assert len(result["actions_applied"]) >= 5

    # Verify that elevated code passes inspector with 100%
    inspector = NeuromorphicInspector()
    post_flaws = inspector.inspect_code(result["elevated_code"])
    assert len(post_flaws) == 0
