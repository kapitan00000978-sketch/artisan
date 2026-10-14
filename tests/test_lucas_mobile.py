"""
Unit tests for Lucas Cruz (Principal Mobile Systems Architect Subsystem).
"""

import pytest
from professions.mobile_systems_architect.references import MobileReferenceLibrary
from professions.mobile_systems_architect.inspector import MobileSystemsInspector
from professions.mobile_systems_architect.rubric import MobileSystemsRubric
from professions.mobile_systems_architect.blind_critic import BlindMobileCritic
from professions.mobile_systems_architect.elevation_engine import MobileSystemsElevationEngine
from professions.mobile_systems_architect.master import LucasCruzMaster


def test_lucas_references_loading():
    frames = MobileReferenceLibrary.get_frame_standards()
    assert "120hz_promotion" in frames
    assert "60hz_standard" in frames
    assert frames["120hz_promotion"]["frame_budget_ms"] <= 8.4

    ergo = MobileReferenceLibrary.get_ergonomic_benchmarks()
    assert ergo["ios_min_touch_target_pt"] >= 44.0
    assert ergo["android_min_touch_target_dp"] >= 48.0

    toxics = MobileReferenceLibrary.get_toxic_anti_patterns()
    assert len(toxics) >= 5
    assert any(t["id"] == "main_thread_blocking_io" for t in toxics)


def test_lucas_inspector_kinetic_app():
    inspector = MobileSystemsInspector()
    kinetic_code = (
        "class ProfileViewController: UIViewController {\n"
        "    func loadProfile() {\n"
        "        DispatchQueue.global(qos: .userInitiated).async { [weak self] in\n"
        "            let user = SQLiteDatabase.shared.loadUser()\n"
        "            DispatchQueue.main.async { [weak self] in\n"
        "                guard let self = self else { return }\n"
        "                self.render(user)\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "    let actionButton = UIButton(frame: CGRect(x: 0, y: 0, width: 48, height: 48))\n"
        "}\n"
    )
    report = inspector.inspect(kinetic_code)
    assert report.is_mobile_viable is True
    assert len(report.critical_violations) == 0
    assert report.metrics.has_main_thread_blocking is False
    assert report.metrics.has_retain_cycles is False
    assert report.metrics.has_offline_caching is True
    assert report.metrics.min_touch_target_dp >= 44.0


def test_lucas_inspector_stuttering_app():
    inspector = MobileSystemsInspector()
    stutter_code = (
        "class BadFeedViewController: UIViewController {\n"
        "    func refresh() {\n"
        "        DispatchQueue.main.sync {\n"
        "            let data = NetworkClient.fetchSync()\n"
        "            self.updateFeed(data)\n"
        "        }\n"
        "    }\n"
        "    let button = UIButton(frame: CGRect(x: 0, y: 0, width: 24, height: 24))\n"
        "}\n"
    )
    report = inspector.inspect(stutter_code)
    assert report.is_mobile_viable is False
    assert len(report.critical_violations) >= 2
    assert report.metrics.has_main_thread_blocking is True
    assert report.metrics.has_offline_caching is False
    assert report.metrics.min_touch_target_dp < 44.0


def test_lucas_rubric_and_veto():
    inspector = MobileSystemsInspector()
    rubric = MobileSystemsRubric()

    blocking_code = (
        "class SettingsView {\n"
        "    func sync() {\n"
        "        DispatchQueue.main.sync { downloadData() }\n"
        "    }\n"
        "}\n"
    )
    report = inspector.inspect(blocking_code)
    evaluation = rubric.evaluate(report)

    assert evaluation.is_certified is False
    assert evaluation.total_score < 85
    assert evaluation.veto_triggered is True
    assert len(evaluation.veto_reasons) > 0


def test_lucas_critic_defect_ledger():
    critic = BlindMobileCritic()
    flawed_code = (
        "class NetworkManager {\n"
        "    func sync() {\n"
        "        DispatchQueue.main.sync { let x = 1 }\n"
        "    }\n"
        "}\n"
    )
    ledger = critic.review(flawed_code)
    assert ledger.verdict == "REJECTED_STUTTER_HAZARD"
    assert ledger.is_certified is False
    assert ledger.fatal_defects_count >= 1
    assert any("FATAL" in d.severity for d in ledger.defects)


def test_lucas_elevation_engine():
    engine = MobileSystemsElevationEngine()
    flawed_code = (
        "class FeedViewController: UIViewController {\n"
        "    func load() {\n"
        "        DispatchQueue.main.sync {\n"
        "            let raw = Network.get()\n"
        "        }\n"
        "    }\n"
        "    let btn = Button(frame: CGRect(width: 28, height: 28))\n"
        "}\n"
    )
    elevated_result = engine.elevate(flawed_code)

    assert elevated_result["status"] == "CERTIFIED"
    assert elevated_result["score"] >= 85
    assert "120HZ BACKGROUND THREAD OFFLOADING" in elevated_result["elevated_mobile"]
    assert "width: 48, height: 48" in elevated_result["elevated_mobile"]


def test_lucas_master_autonomous_cycle():
    master = LucasCruzMaster(passing_threshold=85)
    raw_code = (
        "class FeedComponent {\n"
        "    func refresh() {\n"
        "        DispatchQueue.main.sync { fetch() }\n"
        "    }\n"
        "}\n"
    )
    result = master.run_autonomous_cycle(input_data=raw_code)

    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert "EXECUTIVE MOBILE SYSTEMS BRIEFING" in result["executive_briefing"]
    assert "KINETIC CERTIFIED" in result["executive_briefing"]
