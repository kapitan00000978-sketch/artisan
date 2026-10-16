"""
Test suite validating OASIS SARIF v2.1.0 schema compliance and output generation.
"""

import json
from scripts.detector import to_sarif_v2, scan_code


def test_sarif_structure_clean():
    """Verify SARIF output for clean scan results."""
    clean_result = {
        "passed": True,
        "score": 100,
        "scanned_files": 5,
        "findings": []
    }
    sarif = to_sarif_v2(clean_result)
    assert sarif["version"] == "2.1.0"
    assert "https://raw.githubusercontent.com/oasis-tcs/sarif-spec" in sarif["$schema"]
    assert len(sarif["runs"]) == 1
    run = sarif["runs"][0]
    assert run["tool"]["driver"]["name"] == "Hallwright"
    assert run["results"] == []


def test_sarif_with_findings():
    """Verify SARIF output correctly transforms findings into SARIF results and rules."""
    mock_result = {
        "passed": False,
        "score": 75,
        "scanned_files": 1,
        "findings": [
            {
                "rule_id": "STUB_BARE_EXCEPT",
                "category": "STUB",
                "auditor": "Marcus Sterling",
                "file": "src/api/handler.py",
                "line": 42,
                "matched_text": "except: pass",
                "message": "Silent exception suppression detected.",
                "deduction": 25
            },
            {
                "rule_id": "STUB_TODO",
                "category": "STUB",
                "auditor": "Diana Drake",
                "file": "src/api/handler.py",
                "line": 88,
                "matched_text": "// TODO: fix later",
                "message": "Unfinished stub detected.",
                "deduction": 10
            }
        ]
    }
    sarif = to_sarif_v2(mock_result)
    run = sarif["runs"][0]
    assert len(run["tool"]["driver"]["rules"]) == 2
    assert len(run["results"]) == 2

    # Check first result
    res1 = run["results"][0]
    assert res1["ruleId"] == "STUB_BARE_EXCEPT"
    assert res1["level"] == "error"
    assert res1["locations"][0]["physicalLocation"]["artifactLocation"]["uri"] == "src/api/handler.py"
    assert res1["locations"][0]["physicalLocation"]["region"]["startLine"] == 42

    # Check second result
    res2 = run["results"][1]
    assert res2["ruleId"] == "STUB_TODO"
    assert res2["level"] == "warning"
    assert res2["locations"][0]["physicalLocation"]["region"]["startLine"] == 88
