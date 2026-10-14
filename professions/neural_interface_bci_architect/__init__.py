#!/usr/bin/env python3
"""
Dr. Helena 'The Synapse' Vance: Principal Neural Interface & Biomechatronic BCI Architect
Subsystem Package Initialization
"""

from .references import (
    shannon_safety_limit,
    tissue_temperature_rise,
    electrode_interface_impedance,
    biphasic_charge_balance_error,
    decoding_latency_budget,
    NeuralInterfaceValidationResult,
    validate_neural_interface,
)
from .inspector import NeuralInterfaceInspector
from .rubric import NeuralInterfaceRubric
from .blind_critic import NeuralInterfaceBlindCritic
from .elevation_engine import NeuralInterfaceElevationEngine
from .master import DrHelenaVance

__all__ = [
    "shannon_safety_limit",
    "tissue_temperature_rise",
    "electrode_interface_impedance",
    "biphasic_charge_balance_error",
    "decoding_latency_budget",
    "NeuralInterfaceValidationResult",
    "validate_neural_interface",
    "NeuralInterfaceInspector",
    "NeuralInterfaceRubric",
    "NeuralInterfaceBlindCritic",
    "NeuralInterfaceElevationEngine",
    "DrHelenaVance",
]
