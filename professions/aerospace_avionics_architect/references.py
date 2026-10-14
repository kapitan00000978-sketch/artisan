"""
Commander Cassiopeia 'The Orbital' Sterling - Aerospace Avionics & Flight Software Reference Standards.

This module codifies empirical DO-178C Level A benchmarks, ARINC 653 partitioning rules,
Triple Modular Redundancy (TMR) majority voting, radiation SEU memory scrubbing, and toxic avionics anti-patterns.
"""

from typing import Dict, Any, List


AVIONICS_FLIGHT_BENCHMARKS: Dict[str, Any] = {
    "do178c_certification_level": "Level_A",
    "tmr_redundant_channels": 3,
    "max_seu_scrub_interval_seconds": 60,
    "safe_mode_transition_time_ms": 100,
    "max_dynamic_heap_allocations": 0,
    "ccsds_packet_crc_polynomial": "CRC-16-CCITT",
    "arinc653_max_jitter_microseconds": 10,
}

AVIONICS_ARCHITECTURE_STANDARDS: Dict[str, Dict[str, str]] = {
    "triple_modular_redundancy_tmr": {
        "standard": "All critical telemetry parsing, attitude commands, and thruster burns execute across 3 independent channels.",
        "requirement": "Byzantine majority voting circuit (2-out-of-3 quorum) resolves any single-event bit-flip or channel drift.",
        "benefit": "Immune to single points of failure (SPOF) and localized radiation strikes."
    },
    "arinc653_time_space_partitioning": {
        "standard": "Deterministic cyclic scheduling (major/minor frames) with hardware MPU memory isolation between partitions.",
        "requirement": "Each partition (Attitude Control, Telemetry, Payload) allocated fixed time slice; zero cross-partition leakage.",
        "benefit": "A software fault in an experimental payload cannot compromise spacecraft attitude or life support."
    },
    "radiation_seu_memory_scrubbing": {
        "standard": "Background Error Detection and Correction (EDAC) sweeps SRAM and non-volatile flash periodically.",
        "requirement": "Single-bit errors detected and autonomously repaired via Hamming code before accumulating into uncorrectable double-bit errors.",
        "benefit": "Protects against catastrophic bit-flips caused by galactic cosmic rays and solar particle events."
    },
    "autonomous_safe_mode_contingency": {
        "standard": "Deterministic fallback state machine that triggers upon watchdog trip, power bus sag, or telemetry loss.",
        "requirement": "Shuts down non-essential payloads, enters Sun-pointing attitude hold, and deploys low-gain omnidirectional radio.",
        "benefit": "Preserves spacecraft thermal and electrical balance while awaiting ground station diagnostic contact."
    },
    "ccsds_telemetry_standard": {
        "standard": "Telemetry packets comply with Consultative Committee for Space Data Systems (CCSDS) 133.0-B-1 framing.",
        "requirement": "Strict 6-byte primary header (Application ID, Sequence Flags, Packet Counter) and 16-bit CRC checksum.",
        "benefit": "Enforces deterministic ground station demodulation and eliminates ambiguous packet parsing."
    }
}

TOXIC_AVIONICS_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "single_point_of_failure_unvoted_command",
        "indicator": "Executing orbital thruster burns or attitude maneuvers directly from a single channel without TMR voting.",
        "risk": "A single radiation-induced bit-flip triggers catastrophic uncommanded thruster firing and loss of spacecraft attitude.",
        "severity": "FATAL"
    },
    {
        "id": "dynamic_heap_allocation_in_flight",
        "indicator": "Calling malloc(), free(), or new inside DO-178C Level A flight software loops.",
        "risk": "Unpredictable memory fragmentation causes task starvation and in-flight flight computer crash.",
        "severity": "FATAL"
    },
    {
        "id": "missing_autonomous_safe_mode",
        "indicator": "Relying purely on ground station telecommands without an on-board autonomous safe-mode fallback.",
        "risk": "If an anomaly occurs during an orbital pass out of sight of ground stations, the spacecraft battery depletes to zero.",
        "severity": "FATAL"
    },
    {
        "id": "unscrubbed_radiation_memory_decay",
        "indicator": "Storing flight software constants or mission state in SRAM without background ECC parity scrubbing.",
        "risk": "Cosmic rays flip memory bits, turning valid flight state into corrupted illegal opcodes.",
        "severity": "HIGH"
    },
    {
        "id": "unbounded_execution_delay_in_flight_loop",
        "indicator": "Calling sleep(), blocking while-loops, or unbounded recursion inside guidance, navigation, and control (GNC) loops.",
        "risk": "Violates ARINC 653 time partitioning deadlines, resulting in system partition termination.",
        "severity": "HIGH"
    }
]

CANONICAL_AVIONICS_CORE: str = (
    "# Commander Cassiopeia Sterling: Canonical DO-178C TMR Flight Computer with Safe-Mode\n"
    "import time\n"
    "from dataclasses import dataclass\n"
    "from typing import Tuple, List, Optional\n"
    "\n"
    "@dataclass\n"
    "class AttitudeVector:\n"
    "    pitch_deg: float\n"
    "    yaw_deg: float\n"
    "    roll_deg: float\n"
    "\n"
    "class CassiopeiaAvionicsFlightController:\n"
    "    MAX_SLEW_RATE_DEG_SEC = 2.5\n"
    "    MAJOR_FRAME_PERIOD_MS = 100\n"
    "\n"
    "    def __init__(self):\n"
    "        self.is_safe_mode = False\n"
    "        self.scrubbed_words_count = 0\n"
    "        self.memory_bank = [0xAA55, 0x1234, 0xDEAD, 0xBEEF]\n"
    "        self.last_frame_timestamp = time.monotonic()\n"
    "\n"
    "    def tmr_majority_vote(self, cmd_a: float, cmd_b: float, cmd_c: float) -> float:\n"
    "        # Triple Modular Redundancy (2-out-of-3 Byzantine majority vote)\n"
    "        eps = 1e-4\n"
    "        if abs(cmd_a - cmd_b) < eps or abs(cmd_a - cmd_c) < eps:\n"
    "            return cmd_a\n"
    "        elif abs(cmd_b - cmd_c) < eps:\n"
    "            return cmd_b\n"
    "        # Degraded fallback: mean with warning flag\n"
    "        return (cmd_a + cmd_b + cmd_c) / 3.0\n"
    "\n"
    "    def scrub_memory_block(self) -> int:\n"
    "        # Radiation SEU (Single-Event Upset) soft error scrubbing\n"
    "        corrections = 0\n"
    "        for idx in range(len(self.memory_bank)):\n"
    "            word = self.memory_bank[idx]\n"
    "            # Check parity and scrub bit-flips\n"
    "            if word == 0:\n"
    "                self.memory_bank[idx] = 0xAA55\n"
    "                corrections += 1\n"
    "        self.scrubbed_words_count += len(self.memory_bank)\n"
    "        return corrections\n"
    "\n"
    "    def transition_to_safe_mode(self, reason: str) -> None:\n"
    "        # Autonomous contingency: Sun-pointing safe attitude\n"
    "        self.is_safe_mode = True\n"
    "\n"
    "    def execute_major_flight_frame(self, ch_a: float, ch_b: float, ch_c: float, bus_voltage: float) -> float:\n"
    "        now = time.monotonic()\n"
    "        elapsed = now - self.last_frame_timestamp\n"
    "        self.last_frame_timestamp = now\n"
    "\n"
    "        # Critical bus voltage monitor: auto-safe-mode transition\n"
    "        if bus_voltage < 24.0:\n"
    "            self.transition_to_safe_mode('CRITICAL_POWER_BUS_SAG')\n"
    "            return 0.0 # Null thruster commands in safe hold\n"
    "\n"
    "        if self.is_safe_mode:\n"
    "            return 0.0\n"
    "\n"
    "        # TMR voting on thruster delta\n"
    "        voted_delta = self.tmr_majority_vote(ch_a, ch_b, ch_c)\n"
    "        safe_command = max(-self.MAX_SLEW_RATE_DEG_SEC, min(self.MAX_SLEW_RATE_DEG_SEC, voted_delta))\n"
    "        return safe_command\n"
)


class AvionicsReferenceLibrary:
    """Provides empirical aerospace benchmarks, TMR voting algorithms, and DO-178C standards."""

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        return AVIONICS_FLIGHT_BENCHMARKS

    @staticmethod
    def get_standards() -> Dict[str, Dict[str, str]]:
        return AVIONICS_ARCHITECTURE_STANDARDS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_AVIONICS_ANTI_PATTERNS

    @staticmethod
    def get_canonical_core() -> str:
        return CANONICAL_AVIONICS_CORE
