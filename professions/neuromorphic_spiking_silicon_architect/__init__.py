"""
Neuromorphic Spiking Silicon & Event-Driven Systems Architect Profession Subsystem
Lead Master: Dr. Thalia 'The Synapse' Sterling
"""

from .references import (
    NeuromorphicValidationResult,
    lif_step,
    stdp_weight_update,
    aer_packet_encode,
    aer_packet_decode,
    synaptic_energy_pj,
    validate_neuromorphic_core
)
from .inspector import NeuromorphicInspector
from .rubric import NeuromorphicRubric
from .blind_critic import NeuromorphicBlindCritic
from .elevation_engine import NeuromorphicElevationEngine
from .master import DrThaliaSterling

__all__ = [
    "NeuromorphicValidationResult",
    "lif_step",
    "stdp_weight_update",
    "aer_packet_encode",
    "aer_packet_decode",
    "synaptic_energy_pj",
    "validate_neuromorphic_core",
    "NeuromorphicInspector",
    "NeuromorphicRubric",
    "NeuromorphicBlindCritic",
    "NeuromorphicElevationEngine",
    "DrThaliaSterling"
]
