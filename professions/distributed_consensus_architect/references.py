"""
Soren 'The Conductor' Lindqvist - Distributed Consensus & Protocol Architecture Reference Standards.

This module codifies empirical consensus benchmarks, Raft/Paxos quorum invariants,
Byzantine fault tolerance ratios, re-entrancy defense patterns, and anti-split-brain fencing rules.
"""

from typing import Dict, Any, List


CONSENSUS_PROTOCOL_BENCHMARKS: Dict[str, Any] = {
    "min_quorum_percentage": 51.0,
    "max_election_timeout_ms": 300,
    "min_heartbeat_frequency_ms": 50,
    "byzantine_fault_threshold": 0.333,  # Tolerates f < N/3 Byzantine nodes
    "crash_fault_threshold": 0.50,       # Tolerates f < N/2 Crash nodes
    "reentrancy_guard_enforced": True,
    "deterministic_transition_enforced": True,
}

CONSENSUS_ALGORITHM_STANDARDS: Dict[str, Dict[str, str]] = {
    "raft_consensus": {
        "standard": "Leader-based log replication with randomized election timers and monotonic terms.",
        "invariant": "Log Matching Property & Leader Completeness: If a log entry is committed in a term, it is present in all higher-term leaders.",
        "fencing": "Reject any RPC where term < currentTerm; step down to Follower if term > currentTerm."
    },
    "byzantine_fault_tolerance": {
        "standard": "PBFT / Tendermint 3-phase consensus (Pre-prepare, Prepare, Commit).",
        "invariant": "Safety guaranteed across asynchronous networks if strictly fewer than 1/3 nodes are Byzantine.",
        "fencing": "2/3+ cryptographic commit signatures required before ledger state mutation."
    },
    "smart_contract_state_safety": {
        "standard": "Checks-Effects-Interactions (CEI) & Mutex Re-entrancy Lock.",
        "invariant": "Internal balance and state changes committed prior to any external contract call or value transfer.",
        "fencing": "NonReentrant modifier or atomic reentrancy guard variable."
    }
}

TOXIC_CONSENSUS_ANTI_PATTERNS: List[Dict[str, str]] = [
    {
        "id": "split_brain_minority_write",
        "indicator": "Committing write transactions without confirming strict majority quorum (N/2 + 1) acknowledgments.",
        "risk": "Network partitions cause dual divergent ledgers, irrecoverable state divergence, and catastrophic double-spending.",
        "severity": "FATAL"
    },
    {
        "id": "reentrancy_state_mutation",
        "indicator": "Transferring funds or invoking external callbacks before updating internal storage balances.",
        "risk": "Malicious contracts re-enter state-altering functions recursively, draining vaults and ledgers (e.g. DAO hack).",
        "severity": "FATAL"
    },
    {
        "id": "nondeterministic_state_transition",
        "indicator": "Using system wall clock (Date.now, time.time) or hardware random number generators inside transition functions.",
        "risk": "Different nodes compute different post-state hashes, causing consensus failure and permanent network fork.",
        "severity": "FATAL"
    },
    {
        "id": "stale_term_leader_replay",
        "indicator": "Processing leader commands without verifying monotonic term generation fencing tokens.",
        "risk": "Demoted 'zombie' leaders overwrite state after partition heals, destroying fresh consensus records.",
        "severity": "HIGH"
    },
    {
        "id": "unbounded_gossip_broadcast",
        "indicator": "Flooding consensus proposals recursively across peer mesh without Bloom filters or message dedup caches.",
        "risk": "Causes exponential broadcast storm, choking network bandwidth and causing heartbeat timeouts.",
        "severity": "HIGH"
    }
]

CANONICAL_CONSENSUS_CORE: str = (
    "# Soren Lindqvist: Canonical Fault-Tolerant Consensus State Machine with Term Fencing\n"
    "from dataclasses import dataclass, field\n"
    "from typing import Dict, List, Optional, Set\n"
    "import hashlib\n"
    "\n"
    "@dataclass\n"
    "class LogEntry:\n"
    "    term: int\n"
    "    index: int\n"
    "    command: str\n"
    "    prev_hash: str\n"
    "\n"
    "class ConsensusStateMachine:\n"
    "    def __init__(self, node_id: str, cluster_nodes: List[str]):\n"
    "        self.node_id = node_id\n"
    "        self.cluster_nodes = cluster_nodes\n"
    "        self.cluster_size = len(cluster_nodes)\n"
    "        self.current_term = 0\n"
    "        self.voted_for: Optional[str] = None\n"
    "        self.log: List[LogEntry] = []\n"
    "        self.commit_index = 0\n"
    "        self.state_balances: Dict[str, int] = {}\n"
    "        self._is_reentrant_locked = False\n"
    "\n"
    "    def quorum_size(self) -> int:\n"
    "        return (self.cluster_size // 2) + 1\n"
    "\n"
    "    def apply_transition(self, entry: LogEntry, acks: Set[str]) -> bool:\n"
    "        # Check 1: Term fencing token validation\n"
    "        if entry.term < self.current_term:\n"
    "            return False\n"
    "        # Check 2: Strict majority quorum verification\n"
    "        if len(acks) < self.quorum_size():\n"
    "            return False\n"
    "        # Check 3: Mutex Re-entrancy guard & CEI\n"
    "        if self._is_reentrant_locked:\n"
    "            raise RuntimeError('Re-entrancy violation blocked')\n"
    "        self._is_reentrant_locked = True\n"
    "        try:\n"
    "            # Deterministic state application\n"
    "            self.log.append(entry)\n"
    "            self.commit_index = entry.index\n"
    "            return True\n"
    "        finally:\n"
    "            self._is_reentrant_locked = False\n"
)


class ConsensusReferenceLibrary:
    """Provides empirical distributed consensus benchmarks, quorum invariants, and anti-split-brain standards."""

    @staticmethod
    def get_protocol_benchmarks() -> Dict[str, Any]:
        return CONSENSUS_PROTOCOL_BENCHMARKS

    @staticmethod
    def get_algorithm_standards() -> Dict[str, Dict[str, str]]:
        return CONSENSUS_ALGORITHM_STANDARDS

    @staticmethod
    def get_toxic_anti_patterns() -> List[Dict[str, str]]:
        return TOXIC_CONSENSUS_ANTI_PATTERNS

    @staticmethod
    def get_canonical_consensus_core() -> str:
        return CANONICAL_CONSENSUS_CORE
