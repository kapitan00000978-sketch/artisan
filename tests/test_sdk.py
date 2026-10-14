import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "sdk")))
from craftsman import CraftsmanAgent, COUNCIL_MEMBERS

def test_sdk_council_initialization():
    agent = CraftsmanAgent(persona="software_architect", min_passing_score=95)
    assert "Marcus" in agent.member["name"]
    assert agent.min_passing_score == 95

def test_sdk_execution_lifecycle():
    agent = CraftsmanAgent(persona="software_architect")
    result = agent.execute("Implement rate-limited authentication service")
    assert result["status"] == "certified"
    assert result["score"] >= 95
    assert "Marcus" in result["master"]
    assert len(result["repaired_flaws"]) > 0

def test_sdk_all_council_members_registered():
    assert len(COUNCIL_MEMBERS) == 34
    keys = [
        "software_architect", "elite_copywriter", "principal_designer",
        "startup_cfo_analyst", "legal_contract_auditor", "data_scientist_ml",
        "cyber_security_auditor", "devops_cloud_architect", "spatial_3d_artist",
        "game_systems_architect", "mobile_systems_architect", "brand_identity_director",
        "interactive_sound_architect", "database_distributed_architect", "growth_seo_engineer",
        "ai_agentic_architect", "systems_performance_engineer", "distributed_consensus_architect",
        "compiler_type_architect", "quantum_zkp_cryptographer", "hft_event_loop_architect",
        "robotics_embodied_ai_architect", "hardware_chip_architect", "embedded_firmware_architect",
        "aerospace_avionics_architect", "bioinformatics_genomics_architect", "quantum_hardware_architect",
        "nuclear_criticality_architect", "fusion_plasma_architect", "deep_sea_subsea_architect",
        "hypersonic_aerodynamics_architect", "particle_accelerator_architect", "synthetic_biology_architect",
        "interplanetary_astrodynamics_architect"
    ]
    for k in keys:
        assert k in COUNCIL_MEMBERS
        assert "name" in COUNCIL_MEMBERS[k]
        assert "motto" in COUNCIL_MEMBERS[k]


