"""
Unit tests for Thaddeus 'The Chrono' Vance (Principal HFT & Deterministic Event-Loop Architect Subsystem).
"""

import pytest
from professions.hft_event_loop_architect.references import (
    HftReferenceLibrary,
    CANONICAL_HFT_CORE,
)
from professions.hft_event_loop_architect.inspector import HftSystemInspector
from professions.hft_event_loop_architect.rubric import HftEventLoopRubric
from professions.hft_event_loop_architect.blind_critic import BlindHftCritic
from professions.hft_event_loop_architect.elevation_engine import HftElevationEngine
from professions.hft_event_loop_architect.master import ThaddeusVanceMaster


def test_thaddeus_references_loading():
    benchmarks = HftReferenceLibrary.get_benchmarks()
    assert benchmarks["target_tick_to_trade_nanoseconds"] == 450
    assert benchmarks["max_hot_loop_syscalls"] == 0
    assert benchmarks["core_pinning_required"] is True
    assert benchmarks["lock_free_spsc_ring_buffer"] is True

    standards = HftReferenceLibrary.get_standards()
    assert "kernel_bypass_networking" in standards
    assert "cpu_core_isolation_pinning" in standards
    assert "lock_free_spsc_queue" in standards

    anti_patterns = HftReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "blocking_syscall_on_hot_path" for ap in anti_patterns)


def test_thaddeus_inspector_clean_code():
    inspector = HftSystemInspector()
    report = inspector.inspect(CANONICAL_HFT_CORE)

    assert report.is_hft_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_core_affinity_pinning is True
    assert report.metrics.has_lock_free_ring_buffer is True
    assert report.metrics.has_zero_syscall_polling is True
    assert report.metrics.has_blocking_syscall_or_sleep is False
    assert report.metrics.has_mutex_lock_in_loop is False


def test_thaddeus_inspector_flawed_code():
    inspector = HftSystemInspector()
    flawed_code = (
        "def on_tick(tick):\n"
        "    with lock:\n"
        "        time.sleep(0.001)\n"
        "        order = new Order(tick)\n"
        "        return order\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_hft_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_blocking_syscall_or_sleep is True
    assert report.metrics.has_mutex_lock_in_loop is True
    assert report.metrics.has_core_affinity_pinning is False


def test_thaddeus_rubric_and_veto():
    inspector = HftSystemInspector()
    rubric = HftEventLoopRubric()

    bad_code = (
        "def process_order(msg):\n"
        "    time.sleep(0.0001)\n"
    )
    report = inspector.inspect(bad_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 1
    assert any("Blocking Syscall on Hot Path" in r for r in evaluation.veto_reasons)


def test_thaddeus_critic_defect_ledger():
    critic = BlindHftCritic()
    flawed_code = (
        "def match_engine():\n"
        "    mutex.lock();\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.verdict == "REJECTED_JITTER_LATENCY_HELL"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_thaddeus_elevation_engine():
    engine = HftElevationEngine()
    flawed_code = (
        "class OrderRouter:\n"
        "    def route(self, tick):\n"
        "        with lock:\n"
        "            time.sleep(0.00001)\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "time.sleep" not in elevated_result["elevated_code"]
    assert "bind_thread_affinity" in elevated_result["elevated_code"]
    assert "poll_next_tick" in elevated_result["elevated_code"]


def test_thaddeus_master_autonomous_cycle():
    master = ThaddeusVanceMaster(passing_threshold=85)
    raw_code = (
        "class RawEventLoop:\n"
        "    def handle_tick(self, tick):\n"
        "        return True\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE HFT EVENT-LOOP BRIEFING" in result["executive_briefing"]
    assert "LOW-JITTER DETERMINISM CERTIFIED" in result["executive_briefing"]
