"""Pulsed Power Terawatt Z-Pinch Plasma Confinement Master Subsystem.

Embodying the domain mastery of Dr. Thaddeus 'The Pulse' Vance.
"""

from professions.pulsed_power_terawatt_plasma_architect.references import (
    PulsedPowerParameters,
    PulsedPowerValidationResult,
    validate_pulsed_power_parameters,
    calculate_magnetic_pressure_mbar,
    calculate_convergence_ratio,
    calculate_stagnation_axial_field_tesla,
    calculate_water_breakdown_field_mv_cm,
    calculate_peak_electrical_power_tw,
    MIN_PEAK_CURRENT_MA,
    MAX_RISE_TIME_NS,
    MIN_PEAK_POWER_TW,
    MIN_MAGNETIC_PRESSURE_MBAR,
    MIN_PRESEED_BFIELD_TESLA,
    MIN_LASER_PREHEAT_ENERGY_KJ,
    MIN_CONVERGENCE_RATIO,
    MAX_CONVERGENCE_RATIO,
    MAX_MRT_AMPLITUDE_RATIO,
    MAX_SWITCH_JITTER_NS,
    MIN_ENERGY_DENSITY_KJ_M3,
    MIN_STAGNATION_TEMP_KEV,
    MIN_NEUTRON_YIELD,
)
from professions.pulsed_power_terawatt_plasma_architect.inspector import PulsedPowerCodeInspector
from professions.pulsed_power_terawatt_plasma_architect.rubric import (
    PulsedPowerRubricEvaluator,
    PulsedPowerEvaluationReport,
    CriterionResult,
    PASSING_SCORE_THRESHOLD,
)
from professions.pulsed_power_terawatt_plasma_architect.blind_critic import (
    PulsedPowerBlindCritic,
    BlindCriticVerdict,
)
from professions.pulsed_power_terawatt_plasma_architect.elevation_engine import PulsedPowerElevationEngine
from professions.pulsed_power_terawatt_plasma_architect.master import PulsedPowerMaster

__all__ = [
    "PulsedPowerParameters",
    "PulsedPowerValidationResult",
    "validate_pulsed_power_parameters",
    "calculate_magnetic_pressure_mbar",
    "calculate_convergence_ratio",
    "calculate_stagnation_axial_field_tesla",
    "calculate_water_breakdown_field_mv_cm",
    "calculate_peak_electrical_power_tw",
    "MIN_PEAK_CURRENT_MA",
    "MAX_RISE_TIME_NS",
    "MIN_PEAK_POWER_TW",
    "MIN_MAGNETIC_PRESSURE_MBAR",
    "MIN_PRESEED_BFIELD_TESLA",
    "MIN_LASER_PREHEAT_ENERGY_KJ",
    "MIN_CONVERGENCE_RATIO",
    "MAX_CONVERGENCE_RATIO",
    "MAX_MRT_AMPLITUDE_RATIO",
    "MAX_SWITCH_JITTER_NS",
    "MIN_ENERGY_DENSITY_KJ_M3",
    "MIN_STAGNATION_TEMP_KEV",
    "MIN_NEUTRON_YIELD",
    "PulsedPowerCodeInspector",
    "PulsedPowerRubricEvaluator",
    "PulsedPowerEvaluationReport",
    "CriterionResult",
    "PASSING_SCORE_THRESHOLD",
    "PulsedPowerBlindCritic",
    "BlindCriticVerdict",
    "PulsedPowerElevationEngine",
    "PulsedPowerMaster",
]
