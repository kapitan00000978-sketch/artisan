"""
Tests for AgentRegistry (Multi-Agent State Synchronization).
Verifies registration, heartbeat, timeout pruning, release, and conflict checking.
"""

import os
import sys
import tempfile
from datetime import datetime, timezone, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "src", "sdk"))

from agent_registry import AgentRegistry


def test_agent_registry_lifecycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        sess_file = os.path.join(tmpdir, "sessions.json")
        reg = AgentRegistry(sessions_path=sess_file)

        # 1. Register
        sess = reg.register_session(
            agent_name="Claude Code",
            active_files=["src/api.py", "src/auth.py"],
            intent="Refactoring auth flow"
        )
        assert sess["agent_name"] == "Claude Code"
        assert len(sess["active_files"]) == 2
        sid = sess["session_id"]

        # 2. Get active sessions
        active = reg.get_active_sessions()
        assert len(active) == 1
        assert active[0]["session_id"] == sid

        # 3. Heartbeat
        assert reg.heartbeat(sid)

        # 4. Conflict check
        conflicts = reg.check_conflicts(target_file="src/api.py", current_session_id="different_session")
        assert len(conflicts) == 1
        assert conflicts[0]["agent_name"] == "Claude Code"

        # No conflict for own session
        no_conflicts = reg.check_conflicts(target_file="src/api.py", current_session_id=sid)
        assert len(no_conflicts) == 0

        # No conflict for untouched file
        unrelated = reg.check_conflicts(target_file="docs/README.md")
        assert len(unrelated) == 0

        # 5. Release
        assert reg.release_session(sid)
        assert len(reg.get_active_sessions()) == 0


def test_agent_registry_prunes_stale_sessions():
    with tempfile.TemporaryDirectory() as tmpdir:
        sess_file = os.path.join(tmpdir, "sessions.json")
        reg = AgentRegistry(sessions_path=sess_file)

        sess = reg.register_session(agent_name="Ghost Agent", intent="Stale session test")
        sid = sess["session_id"]

        # Manually alter the heartbeat to 30 minutes in the past
        data = reg._read_data()
        stale_time = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
        for s in data["active_sessions"]:
            if s["session_id"] == sid:
                s["last_heartbeat"] = stale_time
        reg._write_atomic(data)

        # Query with 15-minute timeout should prune it
        active = reg.get_active_sessions(timeout_minutes=15)
        assert len(active) == 0
