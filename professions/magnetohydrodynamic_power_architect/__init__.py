"""
Dr. Evander 'The Plasma-Torch' Sterling - Principal Magnetohydrodynamic Energy Conversion & Direct Space-Power Architect.
Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    VACUUM_PERMEABILITY,
    ELEMENTARY_CHARGE,
    ELECTRON_MASS,
    BOLTZMANN_CONSTANT,
    MIN_POWER_DENSITY_W_M3,
    MAX_HALL_PARAMETER,
    MIN_STUART_NUMBER,
    MAX_STUART_NUMBER,
    MIN_ENTHALPY_EXTRACTION,
    MAX_HALL_ELECTRIC_FIELD_V_M,
    MAX_SHEATH_VOLTAGE_DROP_V,
    MIN_LOAD_FACTOR,
    MAX_LOAD_FACTOR,
    calculate_hall_parameter,
    calculate_effective_conductivity,
    calculate_power_density,
    calculate_stuart_number,
    calculate_hall_electric_field,
    calculate_enthalpy_extraction,
    MhdPowerValidationResult,
    validate_mhd_power_generator,
)

from .inspector import MhdPowerInspector
from .rubric import MhdPowerRubric, RubricEvaluation
from .blind_critic import MhdPowerBlindCritic
from .elevation_engine import MhdPowerElevationEngine
from .master import MhdPowerMaster

__all__ = [
    "VACUUM_PERMEABILITY",
    "ELEMENTARY_CHARGE",
    "ELECTRON_MASS",
    "BOLTZMANN_CONSTANT",
    "MIN_POWER_DENSITY_W_M3",
    "MAX_HALL_PARAMETER",
    "MIN_STUART_NUMBER",
    "MAX_STUART_NUMBER",
    "MIN_ENTHALPY_EXTRACTION",
    "MAX_HALL_ELECTRIC_FIELD_V_M",
    "MAX_SHEATH_VOLTAGE_DROP_V",
    "MIN_LOAD_FACTOR",
    "MAX_LOAD_FACTOR",
    "calculate_hall_parameter",
    "calculate_effective_conductivity",
    "calculate_power_density",
    "calculate_stuart_number",
    "calculate_hall_electric_field",
    "calculate_enthalpy_extraction",
    "MhdPowerValidationResult",
    "validate_mhd_power_generator",
    "MhdPowerInspector",
    "MhdPowerRubric",
    "RubricEvaluation",
    "MhdPowerBlindCritic",
    "MhdPowerElevationEngine",
    "MhdPowerMaster",
]
