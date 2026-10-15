"""Dr. Eliana 'The Chrono-Metrology' Sterling - Principal Optical Lattice Atomic Clock & Quantum Metrology Architect.

Exports references, inspector, rubric, blind critic, elevation engine, and master controller.
"""

from .references import (
    SPEED_OF_LIGHT,
    PLANCK_CONSTANT,
    REDUCED_PLANCK,
    BOLTZMANN_CONSTANT,
    STANDARD_GRAVITY,
    SR87_CLOCK_TRANSITION_FREQ_HZ,
    SR87_CLOCK_TRANSITION_WAVELENGTH_NM,
    SR87_MAGIC_WAVELENGTH_NM,
    YB171_MAGIC_WAVELENGTH_NM,
    MAX_FRACTIONAL_INACCURACY,
    MAX_ALLAN_DEV_COEFF,
    MAX_MAGIC_WAVELENGTH_DETUNING_NM,
    MAX_LASER_LINEWIDTH_MHZ,
    MIN_CAVITY_FINESSE,
    MIN_SILICON_CAVITY_TEMP_K,
    MAX_SILICON_CAVITY_TEMP_K,
    MAX_BBR_TEMP_UNCERTAINTY_MK,
    MAX_ATOM_TEMPERATURE_UK,
    MAX_COLLISIONAL_SHIFT_FRACTION,
    MAX_RESIDUAL_ZEEMAN_UT,
    calculate_gravitational_redshift_fraction,
    calculate_allan_deviation,
    calculate_ac_stark_shift_fraction,
    calculate_quantum_projection_noise_limit,
    OpticalClockValidationResult,
    validate_optical_clock_parameters,
)

from .inspector import OpticalClockInspector
from .rubric import OpticalClockRubric, RubricEvaluation
from .blind_critic import OpticalClockBlindCritic
from .elevation_engine import OpticalClockElevationEngine
from .master import OpticalClockMaster

__all__ = [
    "SPEED_OF_LIGHT",
    "PLANCK_CONSTANT",
    "REDUCED_PLANCK",
    "BOLTZMANN_CONSTANT",
    "STANDARD_GRAVITY",
    "SR87_CLOCK_TRANSITION_FREQ_HZ",
    "SR87_CLOCK_TRANSITION_WAVELENGTH_NM",
    "SR87_MAGIC_WAVELENGTH_NM",
    "YB171_MAGIC_WAVELENGTH_NM",
    "MAX_FRACTIONAL_INACCURACY",
    "MAX_ALLAN_DEV_COEFF",
    "MAX_MAGIC_WAVELENGTH_DETUNING_NM",
    "MAX_LASER_LINEWIDTH_MHZ",
    "MIN_CAVITY_FINESSE",
    "MIN_SILICON_CAVITY_TEMP_K",
    "MAX_SILICON_CAVITY_TEMP_K",
    "MAX_BBR_TEMP_UNCERTAINTY_MK",
    "MAX_ATOM_TEMPERATURE_UK",
    "MAX_COLLISIONAL_SHIFT_FRACTION",
    "MAX_RESIDUAL_ZEEMAN_UT",
    "calculate_gravitational_redshift_fraction",
    "calculate_allan_deviation",
    "calculate_ac_stark_shift_fraction",
    "calculate_quantum_projection_noise_limit",
    "OpticalClockValidationResult",
    "validate_optical_clock_parameters",
    "OpticalClockInspector",
    "OpticalClockRubric",
    "RubricEvaluation",
    "OpticalClockBlindCritic",
    "OpticalClockElevationEngine",
    "OpticalClockMaster",
]
