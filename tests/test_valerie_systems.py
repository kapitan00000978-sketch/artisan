"""
Unit tests for Valerie 'The Edge' Cross (Principal Systems & Low-Level Performance Architect Subsystem).
"""

import pytest
from professions.systems_performance_engineer.references import (
    SystemsReferenceLibrary,
    CANONICAL_PERFORMANCE_CORE,
)
from professions.systems_performance_engineer.inspector import SystemsPerformanceInspector
from professions.systems_performance_engineer.rubric import SystemsPerformanceRubric
from professions.systems_performance_engineer.blind_critic import BlindSystemsCritic
from professions.systems_performance_engineer.elevation_engine import SystemsElevationEngine
from professions.systems_performance_engineer.master import ValerieCrossMaster


def test_valerie_references_loading():
    benchmarks = SystemsReferenceLibrary.get_system_benchmarks()
    assert benchmarks["cache_line_size_bytes"] == 64
    assert benchmarks["max_hot_loop_heap_allocations"] == 0
    assert benchmarks["target_l1_cache_hit_rate"] == 0.95

    standards = SystemsReferenceLibrary.get_cache_standards()
    assert "cpu_cache_line" in standards
    assert "zero_copy_views" in standards
    assert "alignas(64)" in standards["cpu_cache_line"]["directive_cpp"]

    anti_patterns = SystemsReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "heap_allocation_in_inner_loop" for ap in anti_patterns)


def test_valerie_inspector_clean_code():
    inspector = SystemsPerformanceInspector()
    report = inspector.inspect(CANONICAL_PERFORMANCE_CORE)

    assert report.is_systems_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_cache_line_alignment is True
    assert report.metrics.has_zero_allocation_hot_loop is True
    assert report.metrics.has_heap_alloc_in_loop is False
    assert report.metrics.has_zero_copy_slices is True
    assert report.metrics.has_simd_or_branchless_optimization is True


def test_valerie_inspector_flawed_code():
    inspector = SystemsPerformanceInspector()
    flawed_code = (
        "struct ThreadState {\n"
        "    atomic<int> counter1;\n"
        "    atomic<int> counter2;\n"
        "};\n"
        "void process_loop(int n) {\n"
        "    for (int i = 0; i < n; ++i) {\n"
        "        auto buffer = new char[1024];\n"
        "        // heap alloc in inner loop\n"
        "    }\n"
        "}\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_systems_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_heap_alloc_in_loop is True
    assert report.metrics.has_false_sharing_vulnerability is True
    assert report.metrics.has_cache_line_alignment is False


def test_valerie_rubric_and_veto():
    inspector = SystemsPerformanceInspector()
    rubric = SystemsPerformanceRubric()

    bad_code = (
        "for (int i = 0; i < count; ++i) {\n"
        "    malloc(256);\n"
        "}\n"
    )
    report = inspector.inspect(bad_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 1
    assert any("Heap Allocation in Hot Loop" in r for r in evaluation.veto_reasons)


def test_valerie_critic_defect_ledger():
    critic = BlindSystemsCritic()
    flawed_code = (
        "void hot_worker() {\n"
        "    while (active) {\n"
        "        std::string s = compute();\n"
        "        new Item(s);\n"
        "    }\n"
        "}\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.verdict == "REJECTED_SILICON_STRANGULATION"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_valerie_elevation_engine():
    engine = SystemsElevationEngine()
    flawed_code = (
        "struct WorkerNode {\n"
        "    int id;\n"
        "};\n"
        "void run_batch(std::vector<int> data) {\n"
        "    for (int i = 0; i < data.size(); ++i) {\n"
        "        int* tmp = new int[64];\n"
        "        delete[] tmp;\n"
        "    }\n"
        "}\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "alignas(64)" in elevated_result["elevated_code"]
    assert "std::span" in elevated_result["elevated_code"] or "span" in elevated_result["elevated_code"]
    assert "preallocated" in elevated_result["elevated_code"] or "stack_arena" in elevated_result["elevated_code"]


def test_valerie_master_autonomous_cycle():
    master = ValerieCrossMaster(passing_threshold=85)
    raw_code = (
        "struct State {\n"
        "    int counter;\n"
        "};\n"
        "void loop() {\n"
        "    for (int i = 0; i < 1000; i++) {\n"
        "        malloc(32);\n"
        "    }\n"
        "}\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE LOW-LEVEL SYSTEMS BRIEFING" in result["executive_briefing"]
    assert "MECHANICAL SYMPATHY CERTIFIED" in result["executive_briefing"]
