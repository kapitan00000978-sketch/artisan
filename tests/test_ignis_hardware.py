"""
Unit tests for Ignis 'The Silicon' Thorne (Principal ASIC & FPGA Hardware Architect Subsystem).
"""

import pytest
from professions.hardware_chip_architect.references import (
    HardwareReferenceLibrary,
    HARDWARE_TIMING_BENCHMARKS,
    CANONICAL_HARDWARE_CORE,
)
from professions.hardware_chip_architect.inspector import HardwareSystemInspector
from professions.hardware_chip_architect.rubric import HardwareRubric
from professions.hardware_chip_architect.blind_critic import BlindHardwareCritic
from professions.hardware_chip_architect.elevation_engine import HardwareElevationEngine
from professions.hardware_chip_architect.master import IgnisThorneMaster


def test_ignis_references_loading():
    benchmarks = HardwareReferenceLibrary.get_benchmarks()
    assert benchmarks["min_setup_slack_picoseconds"] == 50
    assert benchmarks["cdc_synchronizer_stages"] == 2
    assert benchmarks["inferred_latches_allowed"] == 0

    standards = HardwareReferenceLibrary.get_standards()
    assert "latch_free_combinational_logic" in standards
    assert "dual_flop_cdc_synchronization" in standards
    assert "asynchronous_reset_synchronous_release" in standards
    assert "glitch_free_fsm_architecture" in standards

    anti_patterns = HardwareReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "inferred_latch_in_combinational_block" for ap in anti_patterns)


def test_ignis_inspector_clean_code():
    inspector = HardwareSystemInspector()
    report = inspector.inspect(CANONICAL_HARDWARE_CORE)

    assert report.is_hardware_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_cdc_synchronizer is True
    assert report.metrics.has_latch_free_combinational_logic is True
    assert report.metrics.has_synchronized_reset_deassertion is True
    assert report.metrics.has_glitch_free_fsm is True
    assert report.metrics.has_inferred_latch_risk is False
    assert report.metrics.has_unsynchronized_cdc_risk is False


def test_ignis_inspector_flawed_code():
    inspector = HardwareSystemInspector()
    flawed_rtl = (
        "always @(*) begin\n"
        "    case (sel)\n"
        "        2'b00: out = in0;\n"
        "        2'b01: out = in1;\n"
        "    endcase\n"
        "end\n"
    )
    report = inspector.inspect(flawed_rtl)

    assert report.is_hardware_viable is False
    assert len(report.critical_violations) >= 1
    assert report.metrics.has_inferred_latch_risk is True


def test_ignis_rubric_and_veto():
    inspector = HardwareSystemInspector()
    rubric = HardwareRubric()

    bad_rtl = (
        "always @(*) begin\n"
        "    case (fsm)\n"
        "        2'b00: next = 2'b01;\n"
        "    endcase\n"
        "end\n"
    )
    report = inspector.inspect(bad_rtl)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score <= 45
    assert evaluation.veto_triggered is True
    assert any("INFERRED_TRANSPARENT_LATCH" in r for r in evaluation.veto_reasons)


def test_ignis_critic_defect_ledger():
    critic = BlindHardwareCritic()
    flawed_rtl = (
        "module BadCrossing (input wire clk_a, input wire clk_b, input wire d_in);\n"
        "    always @(posedge clk_b) d_out <= d_in;\n"
        "endmodule\n"
    )
    ledger = critic.review({"code": flawed_rtl, "has_unsynchronized_cdc_risk": True})

    assert ledger.is_certified is False
    assert ledger.score <= 45
    assert any(d.id == "HW-002" for d in ledger.defects)
    assert any("clock domain" in d.description.lower() for d in ledger.defects)


def test_ignis_elevation_engine():
    engine = HardwareElevationEngine()
    flawed_rtl = (
        "module RawModule;\n"
        "    always @(*) begin\n"
        "        case (state)\n"
        "            2'b00: next = 2'b01;\n"
        "        endcase\n"
        "    end\n"
        "endmodule\n"
    )
    elevated_result = engine.elevate(flawed_rtl)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "default:" in elevated_result["elevated_code"]
    assert "cdc_sync_flop" in elevated_result["elevated_code"]
    assert "rst_sync_stage" in elevated_result["elevated_code"]


def test_ignis_master_autonomous_cycle():
    master = IgnisThorneMaster(passing_threshold=85)
    raw_rtl = (
        "module BasicChip (input wire clk);\n"
        "    reg val;\n"
        "endmodule\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_rtl)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE ASIC & FPGA HARDWARE BRIEFING" in result["executive_briefing"]
    assert "SILICON TAPE-OUT CERTIFIED" in result["executive_briefing"]
