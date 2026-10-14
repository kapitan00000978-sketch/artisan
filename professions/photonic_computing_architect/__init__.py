"""
Photonic Computing & Neuromorphic Optical Architect Profession Subsystem
Lead Master: Dr. Corvus 'The Photonic' Vance
"""

from .references import (
    SPEED_OF_LIGHT,
    ELEMENTARY_CHARGE,
    PLANCK_CONSTANT,
    SI_GROUP_INDEX,
    SI_THERMO_OPTIC_COEFF,
    PhotonicValidationResult,
    mzi_transfer_matrix,
    unitary_error_norm,
    thermo_optic_phase_shift,
    optical_mac_latency,
    photodiode_shot_noise_current,
    optical_snr_db,
    validate_photonic_mesh
)
from .inspector import PhotonicInspector
from .rubric import PhotonicRubric
from .blind_critic import PhotonicBlindCritic
from .elevation_engine import PhotonicElevationEngine
from .master import DrCorvusVance

__all__ = [
    "SPEED_OF_LIGHT",
    "ELEMENTARY_CHARGE",
    "PLANCK_CONSTANT",
    "SI_GROUP_INDEX",
    "SI_THERMO_OPTIC_COEFF",
    "PhotonicValidationResult",
    "mzi_transfer_matrix",
    "unitary_error_norm",
    "thermo_optic_phase_shift",
    "optical_mac_latency",
    "photodiode_shot_noise_current",
    "optical_snr_db",
    "validate_photonic_mesh",
    "PhotonicInspector",
    "PhotonicRubric",
    "PhotonicBlindCritic",
    "PhotonicElevationEngine",
    "DrCorvusVance"
]
