"""
Artisan Council of Masters — Guilds and Squads Registry
Organizes the 64 Domain Titans into 8 focused, high-synergy Squads.
"""

from typing import Dict, List, Any

COUNCIL_GUILDS: Dict[str, Dict[str, Any]] = {
    "software_systems": {
        "id": "guild_01",
        "name": "Software & Distributed Systems Guild",
        "lead": "software_architect",
        "icon": "💻",
        "description": "Enterprise backend architecture, databases, distributed consensus, formal compilers, and ultra-low-latency event loops.",
        "members": [
            "software_architect",
            "database_distributed_architect",
            "systems_performance_engineer",
            "distributed_consensus_architect",
            "compiler_type_architect",
            "hft_event_loop_architect"
        ]
    },
    "security_cryptography": {
        "id": "guild_02",
        "name": "Cybersecurity, Zero-Trust & Cryptography Guild",
        "lead": "cyber_security_auditor",
        "icon": "🛡️",
        "description": "Defensive application security, threat modeling, zero-trust perimeter defense, post-quantum ML-KEM lattice cryptography, and zero-knowledge proofs.",
        "members": [
            "cyber_security_auditor",
            "quantum_zkp_cryptographer"
        ]
    },
    "design_multimedia": {
        "id": "guild_03",
        "name": "Design, Spatial 3D & Creative Multimedia Guild",
        "lead": "principal_designer",
        "icon": "🎨",
        "description": "Design systems, spatial UI/UX ergonomics, 3D CGI PBR shaders, game engine physics, mobile 120Hz gesture pipelines, audio acoustics, and brand soul.",
        "members": [
            "principal_designer",
            "spatial_3d_artist",
            "game_systems_architect",
            "mobile_systems_architect",
            "brand_identity_director",
            "interactive_sound_architect"
        ]
    },
    "business_capital_growth": {
        "id": "guild_04",
        "name": "Business, Capital, Growth & Legal Guild",
        "lead": "startup_cfo_analyst",
        "icon": "📈",
        "description": "Startup fractional CFO unit economics, direct-response conversion copywriting, algorithmic Technical SEO growth, and commercial contract litigation defense.",
        "members": [
            "startup_cfo_analyst",
            "elite_copywriter",
            "growth_seo_engineer",
            "legal_contract_auditor"
        ]
    },
    "ai_agentic_neural": {
        "id": "guild_05",
        "name": "AI, Autonomous Agents & Neural Systems Guild",
        "lead": "ai_agentic_architect",
        "icon": "🧠",
        "description": "Deterministic autonomous multi-agent state machines, empirical ML Ops, invasive neural interfaces (BCI), photonic matrix acceleration, and spiking neuromorphic silicon.",
        "members": [
            "ai_agentic_architect",
            "data_scientist_ml",
            "neural_interface_bci_architect",
            "photonic_computing_architect",
            "neuromorphic_spiking_silicon_architect"
        ]
    },
    "hardware_silicon_sre": {
        "id": "guild_06",
        "name": "Hardware, Silicon, Embedded & Cloud SRE Guild",
        "lead": "devops_cloud_architect",
        "icon": "⚡",
        "description": "Cloud SRE and immutable Kubernetes infrastructure, ASIC/FPGA RTL synthesis, bare-metal embedded firmware, real-time autonomous robotics, and High-NA EUV lithography.",
        "members": [
            "devops_cloud_architect",
            "hardware_chip_architect",
            "embedded_firmware_architect",
            "robotics_embodied_ai_architect",
            "extreme_ultraviolet_photolithography_architect"
        ]
    },
    "aerospace_propulsion_orbital": {
        "id": "guild_07",
        "name": "Aerospace, Propulsion & Celestial Dynamics Guild",
        "lead": "aerospace_avionics_architect",
        "icon": "🚀",
        "description": "Fault-tolerant aerospace flight avionics (TMR), hypersonic scramjet aerothermodynamics, interplanetary astrodynamics, thermonuclear fusion rockets, space elevator tensegrity, and mega-constellation orbital safety.",
        "members": [
            "aerospace_avionics_architect",
            "hypersonic_aerodynamics_architect",
            "interplanetary_astrodynamics_architect",
            "fusion_rocket_propulsion_architect",
            "space_elevator_tensegrity_architect",
            "magnetospheric_radiation_shielding_architect",
            "rotating_detonation_wave_propulsion_architect",
            "interstellar_ramjet_bussard_propulsion_architect",
            "megaconstellation_orbital_collision_avoidance_architect",
            "planetary_entry_descent_landing_aerothermodynamics_architect",
            "closed_loop_ecological_life_support_architect"
        ]
    },
    "deep_quantum_nuclear_frontier": {
        "id": "guild_08",
        "name": "Deep Quantum, Nuclear & Frontier Physics Guild",
        "lead": "quantum_hardware_architect",
        "icon": "⚛️",
        "description": "Transmon quantum computing, millikelvin cryogenics, topological spintronics, superfluid quantum hydrodynamics, nuclear criticality safety, tokamak fusion plasma, stellarator magnetics, terawatt pulsed power, and general relativistic astrophysics.",
        "members": [
            "quantum_hardware_architect",
            "cryogenic_superconducting_architect",
            "topological_spintronics_architect",
            "superfluid_hydrodynamics_architect",
            "nuclear_criticality_architect",
            "fusion_plasma_architect",
            "stellarator_twisted_coil_fusion_architect",
            "pulsed_power_terawatt_plasma_architect",
            "particle_accelerator_architect",
            "gravitational_wave_detector_architect",
            "atomic_manipulation_architect",
            "optical_metamaterial_architect",
            "optical_lattice_clock_metrology_architect",
            "deep_sea_subsea_architect",
            "cryovolcanic_hydrothermal_ocean_explorer_architect",
            "bioinformatics_genomics_architect",
            "synthetic_biology_architect",
            "paleogenomic_ancient_dna_reconstruction_architect",
            "exoplanetary_transit_spectroscopy_architect",
            "magnetohydrodynamic_power_architect",
            "planetary_geodynamo_core_architect",
            "extreme_ocean_rogue_wave_hydrodynamics_architect",
            "relativistic_spacetime_geodesic_architect",
            "event_horizon_general_relativistic_magnetohydrodynamics_architect",
            "relativistic_heavy_ion_quark_gluon_plasma_hydrodynamics_architect"
        ]
    }
}


def get_guild_for_master(master_key: str) -> Dict[str, Any]:
    """Finds which guild a master belongs to."""
    for guild_key, guild in COUNCIL_GUILDS.items():
        if master_key in guild["members"]:
            return {"guild_key": guild_key, **guild}
    return {"guild_key": "general", "name": "General Guild", "members": [master_key]}


def list_guilds_summary() -> List[Dict[str, Any]]:
    """Returns a high-level summary of all 8 guilds."""
    summary = []
    for k, g in COUNCIL_GUILDS.items():
        summary.append({
            "key": k,
            "id": g["id"],
            "name": g["name"],
            "icon": g["icon"],
            "lead": g["lead"],
            "member_count": len(g["members"]),
            "description": g["description"]
        })
    return summary
