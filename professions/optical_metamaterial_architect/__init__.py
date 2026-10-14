#!/usr/bin/env python3
"""
Dr. Gideon 'The Refraction' Sterling: Principal Optical Metamaterials & Transformation Optics Architect
Subsystem Package Initialization
"""

from .references import (
    complex_refractive_index,
    optical_figure_of_merit,
    dielectric_loss_tangent,
    srr_resonance_frequency,
    cylindrical_cloak_tensors,
    OpticalMetamaterialValidationResult,
    validate_optical_metamaterial,
)
from .inspector import OpticalMetamaterialInspector
from .rubric import OpticalMetamaterialRubric
from .blind_critic import OpticalMetamaterialBlindCritic
from .elevation_engine import OpticalMetamaterialElevationEngine
from .master import DrGideonSterling

__all__ = [
    "complex_refractive_index",
    "optical_figure_of_merit",
    "dielectric_loss_tangent",
    "srr_resonance_frequency",
    "cylindrical_cloak_tensors",
    "OpticalMetamaterialValidationResult",
    "validate_optical_metamaterial",
    "OpticalMetamaterialInspector",
    "OpticalMetamaterialRubric",
    "OpticalMetamaterialBlindCritic",
    "OpticalMetamaterialElevationEngine",
    "DrGideonSterling",
]
