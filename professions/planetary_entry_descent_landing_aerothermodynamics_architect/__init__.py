"""Planetary Atmospheric Entry, Descent & Landing (EDL) Aerothermodynamics Subsystem.

Formulated by Dr. Caelum 'The Exosphere' Sterling,
Principal Planetary Atmospheric Entry, Descent & Landing (EDL) Aerothermodynamics Architect.
"""

from .references import (
    MIN_ENTRY_VELOCITY_KM_S,
    MAX_ENTRY_VELOCITY_KM_S,
    MIN_ENTRY_MACH,
    MIN_STAGNATION_HEAT_FLUX_MW_M2,
    MIN_TOTAL_HEAT_LOAD_MJ_M2,
    MIN_TPS_SAFETY_FACTOR,
    MAX_BONDLINE_TEMP_C,
    MAX_PEAK_DECELERATION_G,
    MIN_PARACHUTE_DEPLOY_MACH,
    MAX_PARACHUTE_DEPLOY_MACH,
    MIN_PARACHUTE_DYNAMIC_PRESSURE_PA,
    MAX_PARACHUTE_DYNAMIC_PRESSURE_PA,
    MIN_TRN_ALTITUDE_M,
    MAX_LANDING_ELLIPSE_SEMI_MAJOR_M,
    MAX_TOUCHDOWN_VERTICAL_VELOCITY_M_S,
    MAX_TOUCHDOWN_HORIZONTAL_VELOCITY_M_S,
    MIN_PLASMA_RF_MARGIN_DB,
    STANDARD_GRAVITY,
    EDLAerothermodynamicsValidationResult,
    calculate_sutton_graves_stagnation_heat_flux,
    calculate_integrated_heat_load,
    calculate_supersonic_dynamic_pressure,
    calculate_terminal_touchdown_energy,
    calculate_parachute_drag_force,
    validate_edl_parameters,
)
from .inspector import EDLAerothermodynamicsInspector
from .rubric import EDLAerothermodynamicsRubric, PASSING_SCORE
from .blind_critic import EDLAerothermodynamicsBlindCritic
from .elevation_engine import EDLAerothermodynamicsElevationEngine
from .master import EDLAerothermodynamicsMaster, ActiveDecisionJournal

__all__ = [
    "MIN_ENTRY_VELOCITY_KM_S",
    "MAX_ENTRY_VELOCITY_KM_S",
    "MIN_ENTRY_MACH",
    "MIN_STAGNATION_HEAT_FLUX_MW_M2",
    "MIN_TOTAL_HEAT_LOAD_MJ_M2",
    "MIN_TPS_SAFETY_FACTOR",
    "MAX_BONDLINE_TEMP_C",
    "MAX_PEAK_DECELERATION_G",
    "MIN_PARACHUTE_DEPLOY_MACH",
    "MAX_PARACHUTE_DEPLOY_MACH",
    "MIN_PARACHUTE_DYNAMIC_PRESSURE_PA",
    "MAX_PARACHUTE_DYNAMIC_PRESSURE_PA",
    "MIN_TRN_ALTITUDE_M",
    "MAX_LANDING_ELLIPSE_SEMI_MAJOR_M",
    "MAX_TOUCHDOWN_VERTICAL_VELOCITY_M_S",
    "MAX_TOUCHDOWN_HORIZONTAL_VELOCITY_M_S",
    "MIN_PLASMA_RF_MARGIN_DB",
    "STANDARD_GRAVITY",
    "EDLAerothermodynamicsValidationResult",
    "calculate_sutton_graves_stagnation_heat_flux",
    "calculate_integrated_heat_load",
    "calculate_supersonic_dynamic_pressure",
    "calculate_terminal_touchdown_energy",
    "calculate_parachute_drag_force",
    "validate_edl_parameters",
    "EDLAerothermodynamicsInspector",
    "EDLAerothermodynamicsRubric",
    "PASSING_SCORE",
    "EDLAerothermodynamicsBlindCritic",
    "EDLAerothermodynamicsElevationEngine",
    "EDLAerothermodynamicsMaster",
    "ActiveDecisionJournal",
]
