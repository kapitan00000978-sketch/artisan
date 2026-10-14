"""
Unit tests for Naomi Chen (Principal AI Agentic Systems & LLM Architecture Subsystem).
"""

import pytest
from professions.ai_agentic_architect.references import (
    AgenticReferenceLibrary,
    CANONICAL_AGENTIC_LOOP_CORE,
)
from professions.ai_agentic_architect.inspector import AgenticSystemInspector
from professions.ai_agentic_architect.rubric import AgenticArchitectureRubric
from professions.ai_agentic_architect.blind_critic import BlindAgenticCritic
from professions.ai_agentic_architect.elevation_engine import AgenticElevationEngine
from professions.ai_agentic_architect.master import NaomiChenMaster


def test_naomi_references_loading():
    benchmarks = AgenticReferenceLibrary.get_system_benchmarks()
    assert benchmarks["max_iteration_budget"] == 5
    assert benchmarks["min_eval_faithfulness_score"] == 0.90
    assert benchmarks["min_tool_selection_accuracy"] == 0.95

    budgets = AgenticReferenceLibrary.get_context_budgets()
    assert "system_prompt_pct" in budgets
    assert "retrieval_grounding_pct" in budgets
    assert budgets["retrieval_grounding_pct"] == 40.0

    anti_patterns = AgenticReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "unbounded_while_true_agent_loop" for ap in anti_patterns)


def test_naomi_inspector_clean_agent():
    inspector = AgenticSystemInspector()
    report = inspector.inspect(CANONICAL_AGENTIC_LOOP_CORE)

    assert report.is_agentic_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_max_iteration_circuit_breaker is True
    assert report.metrics.has_unbounded_while_loop is False
    assert report.metrics.has_prompt_injection_delimiter is True
    assert report.metrics.has_structured_output_schema is True


def test_naomi_inspector_flawed_agent():
    inspector = AgenticSystemInspector()
    flawed_code = (
        "def rogue_agent(user_input: str):\n"
        "    prompt = f'System: You are an agent. Solve: {user_input}'\n"
        "    while True:\n"
        "        resp = openai.ChatCompletion.create(prompt=prompt)\n"
        "        if 'DONE' in resp:\n"
        "            break\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_agentic_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_unbounded_while_loop is True
    assert report.metrics.has_raw_prompt_fstring_injection is True
    assert report.metrics.has_structured_output_schema is False


def test_naomi_rubric_and_veto():
    inspector = AgenticSystemInspector()
    rubric = AgenticArchitectureRubric()

    bad_agent = (
        "while True:\n"
        "    call_llm(user_input)\n"
    )
    report = inspector.inspect(bad_agent)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) >= 2


def test_naomi_critic_defect_ledger():
    critic = BlindAgenticCritic()
    flawed_code = (
        "def chat(user_input):\n"
        "    while True:\n"
        "        pass\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.verdict == "REJECTED_STOCHASTIC_CHAOS"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_naomi_elevation_engine():
    engine = AgenticElevationEngine()
    flawed_code = (
        "def run_loop(user_input):\n"
        "    prompt = f'User asked: {user_input}'\n"
        "    while True:\n"
        "        result = call_llm(prompt)\n"
        "        if result:\n"
        "            break\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "max_iterations" in elevated_result["elevated_agent"]
    assert "untrusted_input" in elevated_result["elevated_agent"]
    assert "StructuredAgentDecision" in elevated_result["elevated_agent"]


def test_naomi_master_autonomous_cycle():
    master = NaomiChenMaster(passing_threshold=85)
    raw_agent = (
        "def agent_run(user_input: str):\n"
        "    p = f'Execute: {user_input}'\n"
        "    while True:\n"
        "        ans = llm(p)\n"
        "        break\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_agent)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE AI AGENTIC ARCHITECTURE BRIEFING" in result["executive_briefing"]
    assert "DETERMINISTIC AGENT CERTIFIED" in result["executive_briefing"]
