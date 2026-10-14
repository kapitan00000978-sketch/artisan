"""
Unit tests for Nikolai 'The Core' Vance (Principal Compiler & High-Assurance Type Systems Architect Subsystem).
"""

import pytest
from professions.compiler_type_architect.references import (
    CompilerReferenceLibrary,
    CANONICAL_COMPILER_CORE,
)
from professions.compiler_type_architect.inspector import CompilerSystemInspector
from professions.compiler_type_architect.rubric import CompilerTypeRubric
from professions.compiler_type_architect.blind_critic import BlindCompilerCritic
from professions.compiler_type_architect.elevation_engine import CompilerElevationEngine
from professions.compiler_type_architect.master import NikolaiVanceMaster


def test_nikolai_references_loading():
    benchmarks = CompilerReferenceLibrary.get_system_benchmarks()
    assert benchmarks["min_variant_coverage_ratio"] == 1.0
    assert benchmarks["max_ast_recursion_depth"] == 512
    assert benchmarks["allow_unsound_any_casts"] is False

    standards = CompilerReferenceLibrary.get_type_standards()
    assert "algebraic_data_types" in standards
    assert "borrow_checker_safety" in standards
    assert "ssa_intermediate_representation" in standards

    anti_patterns = CompilerReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "non_exhaustive_pattern_matching" for ap in anti_patterns)


def test_nikolai_inspector_clean_code():
    inspector = CompilerSystemInspector()
    report = inspector.inspect(CANONICAL_COMPILER_CORE)

    assert report.is_compiler_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_exhaustive_pattern_matching is True
    assert report.metrics.has_depth_circuit_breaker is True
    assert report.metrics.has_algebraic_result_or_option is True
    assert report.metrics.has_unsound_escape_hatch is False
    assert report.metrics.has_non_exhaustive_matching is False


def test_nikolai_inspector_flawed_code():
    inspector = CompilerSystemInspector()
    flawed_code = (
        "def evaluate(node):\n"
        "    val = node as any\n"
        "    match node.kind:\n"
        "        case 'literal': return val\n"
        "    return evaluate(node.next)\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_compiler_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_unsound_escape_hatch is True
    assert report.metrics.has_non_exhaustive_matching is True
    assert report.metrics.has_unbounded_recursion is True


def test_nikolai_rubric_and_veto():
    inspector = CompilerSystemInspector()
    rubric = CompilerTypeRubric()

    bad_code = (
        "function parseAST(x) {\n"
        "    // @ts-ignore\n"
        "    const unsafeVal = x as any;\n"
        "    return unsafeVal;\n"
        "}\n"
    )
    report = inspector.inspect(bad_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 1
    assert any("Unsound Type Escape Hatch" in r for r in evaluation.veto_reasons)


def test_nikolai_critic_defect_ledger():
    critic = BlindCompilerCritic()
    flawed_code = (
        "def lower_ast(node):\n"
        "    return node as any\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.verdict == "REJECTED_UNSOUND_TYPE_AMBIGUITY"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_nikolai_elevation_engine():
    engine = CompilerElevationEngine()
    flawed_code = (
        "class TypeChecker:\n"
        "    def evaluate(self, node):\n"
        "        raw = node as any\n"
        "        match node.type:\n"
        "            case 'INT': return 1\n"
        "            case 'STR': return 'text'\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "as any" not in elevated_result["elevated_code"]
    assert "case _:" in elevated_result["elevated_code"]
    assert "MAX_SAFE_DEPTH" in elevated_result["elevated_code"]


def test_nikolai_master_autonomous_cycle():
    master = NikolaiVanceMaster(passing_threshold=85)
    raw_code = (
        "class RawCompilerPass:\n"
        "    def evaluate(self, node):\n"
        "        match node.tag:\n"
        "            case 'A': return 1\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE COMPILER & TYPE ARCHITECTURE BRIEFING" in result["executive_briefing"]
    assert "TYPE SOUNDNESS CERTIFIED" in result["executive_briefing"]
