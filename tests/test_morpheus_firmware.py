"""
Unit tests for Morpheus 'The Kernel' Vance (Principal Embedded Firmware Architect Subsystem).
"""

import pytest
from professions.embedded_firmware_architect.references import (
    FirmwareReferenceLibrary,
    FIRMWARE_SYSTEM_BENCHMARKS,
    CANONICAL_FIRMWARE_CORE,
)
from professions.embedded_firmware_architect.inspector import FirmwareSystemInspector
from professions.embedded_firmware_architect.rubric import FirmwareRubric
from professions.embedded_firmware_architect.blind_critic import BlindFirmwareCritic
from professions.embedded_firmware_architect.elevation_engine import FirmwareElevationEngine
from professions.embedded_firmware_architect.master import MorpheusVanceMaster


def test_morpheus_references_loading():
    benchmarks = FirmwareReferenceLibrary.get_benchmarks()
    assert benchmarks["max_isr_duration_microseconds"] == 5.0
    assert benchmarks["max_dynamic_heap_allocations"] == 0
    assert benchmarks["hardware_watchdog_timeout_ms"] == 250

    standards = FirmwareReferenceLibrary.get_standards()
    assert "zero_heap_static_allocation" in standards
    assert "deferred_interrupt_handling" in standards
    assert "dma_cache_coherency_maintenance" in standards
    assert "hardware_watchdog_supervisor" in standards

    anti_patterns = FirmwareReferenceLibrary.get_toxic_anti_patterns()
    assert len(anti_patterns) >= 4
    assert any(ap["id"] == "dynamic_heap_allocation_in_embedded" for ap in anti_patterns)


def test_morpheus_inspector_clean_code():
    inspector = FirmwareSystemInspector()
    report = inspector.inspect(CANONICAL_FIRMWARE_CORE)

    assert report.is_firmware_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_zero_heap_allocation is True
    assert report.metrics.has_hardware_watchdog is True
    assert report.metrics.has_volatile_mmio_registers is True
    assert report.metrics.has_dma_cache_coherency is True
    assert report.metrics.has_dynamic_heap_allocation_risk is False
    assert report.metrics.has_blocking_delay_in_isr is False


def test_morpheus_inspector_flawed_code():
    inspector = FirmwareSystemInspector()
    flawed_code = (
        "void USART_IRQHandler(void) {\n"
        "    char *buf = (char *)malloc(64);\n"
        "    delay_ms(10);\n"
        "}\n"
    )
    report = inspector.inspect(flawed_code)

    assert report.is_firmware_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_dynamic_heap_allocation_risk is True
    assert report.metrics.has_blocking_delay_in_isr is True
    assert report.metrics.has_hardware_watchdog is False


def test_morpheus_rubric_and_veto():
    inspector = FirmwareSystemInspector()
    rubric = FirmwareRubric()

    bad_code = (
        "void process_packet() {\n"
        "    uint8_t *pkt = malloc(128);\n"
        "}\n"
    )
    report = inspector.inspect(bad_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score <= 45
    assert evaluation.veto_triggered is True
    assert any("DYNAMIC_HEAP_ALLOCATION" in r for r in evaluation.veto_reasons)


def test_morpheus_critic_defect_ledger():
    critic = BlindFirmwareCritic()
    flawed_code = (
        "void UART_ISR(void) {\n"
        "    sleep_ms(5);\n"
        "}\n"
    )
    ledger = critic.review(flawed_code)

    assert ledger.is_certified is False
    assert ledger.score <= 45
    assert any(d.id == "FW-002" or d.id == "FW-003" for d in ledger.defects)
    assert any("interrupt" in d.description.lower() or "watchdog" in d.description.lower() for d in ledger.defects)


def test_morpheus_elevation_engine():
    engine = FirmwareElevationEngine()
    flawed_code = (
        "void firmware_run() {\n"
        "    char *temp = malloc(32);\n"
        "    free(temp);\n"
        "}\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "malloc" not in elevated_result["elevated_code"] or "/* Static buffer" in elevated_result["elevated_code"]
    assert "bsp_watchdog_init" in elevated_result["elevated_code"]
    assert "bsp_dma_cache_invalidate" in elevated_result["elevated_code"]


def test_morpheus_master_autonomous_cycle():
    master = MorpheusVanceMaster(passing_threshold=85)
    raw_code = (
        "void main_baremetal(void) {\n"
        "    while (1) {}\n"
        "}\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE EMBEDDED FIRMWARE BRIEFING" in result["executive_briefing"]
    assert "BARE-METAL FIRMWARE CERTIFIED" in result["executive_briefing"]
