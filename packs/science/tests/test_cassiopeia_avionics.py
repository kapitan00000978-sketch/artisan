"""
Unit tests for Commander Cassiopeia 'The Orbital' Sterling (Principal Aerospace Avionics Subsystem).
"""

import pytest
from professions.aerospace_avionics_architect.references import (
    AvionicsReferenceLibrary,
    AVIONICS_FLIGHT_BENCHMARKS,
    CANONICAL_AVIONICS_CORE,
)
from professions.aerospace_avionics_architect.inspector import AvionicsSystemInspector
from professions.aerospace_avionics_architect.rubric import AvionicsRubric
from professions.aerospace_avionics_architect.blind_critic import BlindAvionicsCritic
from professions.aerospace_avionics_architect.elevation_engine import AvionicsElevationEngine
from professions.aerospace_avionics_architect.master import CassiopeiaSterlingMaster


def test_cassiopeia_references_loading():
    benchmarks = AvionicsReferenceLibrary.get_benchmarks()
    assert benchmarks["do178c_certification_level"] == "Level_A"
    assert benchmarks["tmr_redundant_channels"] == 3
    assert benchmarks["max_dynamic_heap_allocations"] == 0

    standards = AvionicsReferenceLibrary.get_standards()
    assert "triple_modular_redundancy_tmr" in standards
    assert "arinc653_time_space_partitioning" in standards
    assert "radiation_seu_memory_scrubbing" in standards
    assert "autonomous_safe_mode_contingency" in standards

    anti_patterns = AvionicsReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "single_point_of_failure_unvoted_command" for ap in anti_patterns)


def test_cassiopeia_inspector_clean_code():
    inspector = AvionicsSystemInspector()
    report = inspector.inspect(CANONICAL_AVIONICS_CORE)

    assert report.is_avionics_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_tmr_majority_voting is True
    assert report.metrics.has_autonomous_safe_mode is True
    assert report.metrics.has_radiation_memory_scrubbing is True
    assert report.metrics.has_deterministic_time_framing is True
    assert report.metrics.has_single_point_of_failure is False
    assert report.metrics.has_dynamic_heap_allocation is False


def test_cassiopeia_inspector_flawed_code():
    inspector = AvionicsSystemInspector()
    flawed_code = (
        "def fire_thruster_direct(delta_v):\n"
        "    time.sleep(0.1)\n"
        "    return delta_v\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_avionics_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_single_point_of_failure is True
    assert report.metrics.has_unbounded_sleep_in_flight_loop is True
    assert report.metrics.has_autonomous_safe_mode is False


def test_cassiopeia_rubric_and_veto():
    inspector = AvionicsSystemInspector()
    rubric = AvionicsRubric()

    bad_code = (
        "def actuate(cmd):\n"
        "    send_thruster_packet(cmd)\n"
    )
    report = inspector.inspect(bad_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score <= 45
    assert evaluation.veto_triggered is True
    assert any("SINGLE_POINT_OF_FAILURE" in r or "MISSING_AUTONOMOUS_SAFE_MODE" in r for r in evaluation.veto_reasons)


def test_cassiopeia_critic_defect_ledger():
    critic = BlindAvionicsCritic()
    flawed_code = (
        "def guidance_loop(delta):\n"
        "    buf = malloc(64)\n"
    )
    ledger = critic.review({"code": flawed_code, "has_dynamic_heap_allocation": True})

    assert ledger.is_certified is False
    assert ledger.score <= 45
    assert any(d.id == "AV-002" or d.id == "AV-003" for d in ledger.defects)
    assert any("heap" in d.description.lower() or "safe-mode" in d.description.lower() for d in ledger.defects)


def test_cassiopeia_elevation_engine():
    engine = AvionicsElevationEngine()
    flawed_code = (
        "class RawFlightGuidance:\n"
        "    def execute_burn(self, delta):\n"
        "        time.sleep(0.01)\n"
        "        return delta\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "tmr_majority_vote" in elevated_result["elevated_code"]
    assert "transition_to_safe_mode" in elevated_result["elevated_code"]
    assert "scrub_memory_block" in elevated_result["elevated_code"]


def test_cassiopeia_master_autonomous_cycle():
    master = CassiopeiaSterlingMaster(passing_threshold=85)
    raw_code = (
        "class BasicSpacecraft:\n"
        "    def run_pass(self):\n"
        "        return True\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE AEROSPACE AVIONICS BRIEFING" in result["executive_briefing"]
    assert "ORBITAL FLIGHT CERTIFIED" in result["executive_briefing"]
