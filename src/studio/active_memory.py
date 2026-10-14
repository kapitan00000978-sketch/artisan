"""
Step 8 — Active Decision Journal & Episodic Memory (Xotira, Haqiqiy)
Active constraint memory:
- Records exact decisions: what was tried, score delta, what worked, what failed.
- Enforces anti-pattern bans: if a strategy failed repeatedly, it is marked FORBIDDEN.
- Constrains future iterations to prevent repetitive loops.
"""

import os
import json
import time
from typing import Dict, Any, List


class ActiveDecisionJournal:
    """
    Episodic Decision Journal that actively constrains future agent actions.
    Ensures the agent learns from scar tissue: 'I made this mistake twice, I won't repeat it'.
    """

    def __init__(self, journal_path: str = ".artisan/decision_journal.json"):
        self.journal_path = journal_path
        self._ensure_journal_exists()

    def _ensure_journal_exists(self):
        os.makedirs(os.path.dirname(self.journal_path), exist_ok=True)
        if not os.path.exists(self.journal_path):
            with open(self.journal_path, "w", encoding="utf-8") as f:
                json.dump({
                    "version": "1.0.0",
                    "records": [],
                    "banned_anti_patterns": [],
                    "proven_successful_strategies": []
                }, f, indent=2)

    def load_journal(self) -> Dict[str, Any]:
        try:
            with open(self.journal_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"records": [], "banned_anti_patterns": [], "proven_successful_strategies": []}

    def record_decision(
        self,
        iteration: int,
        target_file: str,
        defects_before: List[str],
        actions_taken: List[str],
        score_before: float,
        score_after: float
    ) -> Dict[str, Any]:
        """
        Records a decision cycle and actively checks if an action failed repeatedly.
        """
        journal = self.load_journal()
        delta = round(score_after - score_before, 1)

        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "iteration": iteration,
            "target_file": target_file,
            "defects_before": defects_before,
            "actions_taken": actions_taken,
            "score_before": score_before,
            "score_after": score_after,
            "delta": delta,
            "outcome": "SUCCESS" if delta > 0 else ("REGRESSION" if delta < 0 else "NO_IMPACT")
        }

        journal["records"].append(entry)

        # Active constraint enforcement:
        # If an action has zero or negative delta in multiple runs, ban it
        action_outcomes: Dict[str, List[float]] = {}
        for r in journal["records"]:
            for a in r.get("actions_taken", []):
                action_outcomes.setdefault(a, []).append(r.get("delta", 0.0))

        banned = []
        proven = []
        for action, deltas in action_outcomes.items():
            if len(deltas) >= 2 and all(d <= 0 for d in deltas):
                banned.append(action)
            elif any(d >= 10.0 for d in deltas):
                proven.append(action)

        journal["banned_anti_patterns"] = list(set(banned))
        journal["proven_successful_strategies"] = list(set(proven))

        with open(self.journal_path, "w", encoding="utf-8") as f:
            json.dump(journal, f, indent=2)

        return entry

    def is_action_banned(self, action: str) -> bool:
        """Returns True if this remediation was recorded as an ineffective anti-pattern."""
        journal = self.load_journal()
        return action in journal.get("banned_anti_patterns", [])

    def get_proven_strategies(self) -> List[str]:
        journal = self.load_journal()
        return journal.get("proven_successful_strategies", [])
