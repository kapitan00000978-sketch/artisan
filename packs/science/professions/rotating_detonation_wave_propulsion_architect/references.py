"""Physical references and mathematical models for Continuous Rotating Detonation Rocket Engines (RDRE).

Architect: Commander Jaxen 'The Fusion-Torch' Sterling
Domain: rotating_detonation_wave_propulsion_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Fundamental physical constants
UNIVERSAL_GAS_CONSTANT: float = 8.314462618         # J/(mol*K)
STANDARD_GRAVITY: float = 9.80665                   # m/s^2

# Quantitative engineering benchmarks for Rotating Detonation Rocket Engines (RDRE)
MIN_CJ_DETONATION_VELOCITY_M_S: float = 2500.0      # Chapman-Jouguet wave velocity >= 2500 m/s
MIN_CJ_PRESSURE_RATIO: float = 18.0                 # P_CJ / P_0 >= 18.0
MIN_ZND_SPIKE_PRESSURE_RATIO: float = 35.0          # P_ZND / P_0 >= 35.0
MAX_DDT_RUNUP_DISTANCE_MM: float = 15.0             # L_DDT <= 15.0 mm
MIN_DETONATION_FREQUENCY_KHZ: float = 20.0          # f_det >= 20.0 kHz
MIN_CO_ROTATING_WAVES: int = 2                      # n_waves >= 2
MIN_ANNULAR_GAP_MM: float = 2.5                     # Delta r >= 2.5 mm
MAX_ANNULAR_GAP_MM: float = 12.0                    # Delta r <= 12.0 mm
MIN_ANNULAR_DIAMETER_MM: float = 50.0               # D_annulus >= 50.0 mm
MAX_ANNULAR_DIAMETER_MM: float = 300.0              # D_annulus <= 300.0 mm
MIN_PRESSURE_GAIN_EFFICIENCY: float = 0.15          # eta_gain >= 0.15 (15% pressure gain)
MIN_AEROSPIKE_NOZZLE_EFFICIENCY: float = 0.92       # eta_nozzle >= 0.92 (92%)
MIN_SPECIFIC_IMPULSE_S: float = 450.0               # I_sp >= 450.0 s
MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2: float = 35.0      # q_wall <= 35.0 MW/m^2


def calculate_cj_detonation_velocity(
    heat_release_j_kg: float,
    gamma: float = 1.25,
    gas_constant_r: float = 350.0,
    initial_temp_k: float = 300.0
) -> float:
    """Calculate the Chapman-Jouguet detonation front velocity in m/s.

    D_CJ = sqrt( 2*(gamma^2 - 1)*q + 2*gamma*R*T_0 )
    """
    if heat_release_j_kg <= 0.0 or gamma <= 1.0 or gas_constant_r <= 0.0 or initial_temp_k <= 0.0:
        return 0.0

    term1 = 2.0 * ((gamma ** 2) - 1.0) * heat_release_j_kg
    term2 = 2.0 * gamma * gas_constant_r * initial_temp_k
    radicand = term1 + term2
    return math.sqrt(max(0.0, radicand))


def calculate_detonation_frequency(
    cj_velocity_m_s: float,
    annular_diameter_mm: float,
    num_waves: int = 2
) -> float:
    """Calculate the continuous rotating detonation wave frequency in kHz.

    f_det = (num_waves * D_CJ) / (pi * D_annulus_m) / 1000.0
    """
    if cj_velocity_m_s <= 0.0 or annular_diameter_mm <= 0.0 or num_waves <= 0:
        return 0.0

    diameter_m = annular_diameter_mm / 1000.0
    circumference_m = math.pi * diameter_m
    freq_hz = (num_waves * cj_velocity_m_s) / circumference_m
    return freq_hz / 1000.0


def calculate_pressure_gain_ratio(
    exit_total_pressure_mpa: float,
    inlet_total_pressure_mpa: float
) -> float:
    """Calculate thermodynamic pressure gain efficiency over isobaric cycle.

    eta_gain = (P_total_exit - P_total_inlet) / P_total_inlet
    """
    if inlet_total_pressure_mpa <= 0.0 or exit_total_pressure_mpa <= 0.0:
        return 0.0

    gain = (exit_total_pressure_mpa - inlet_total_pressure_mpa) / inlet_total_pressure_mpa
    return max(0.0, gain)


def calculate_aerospike_thrust_efficiency(
    ambient_pressure_kpa: float,
    design_pressure_kpa: float = 101.325,
    base_efficiency: float = 0.96
) -> float:
    """Calculate altitude-compensating truncated aerospike nozzle expansion efficiency."""
    if ambient_pressure_kpa < 0.0 or design_pressure_kpa <= 0.0:
        return 0.0

    # Truncated aerospike maintains near constant high efficiency across varying backpressures
    pr = ambient_pressure_kpa / design_pressure_kpa
    if pr > 1.0:
        # Overexpanded near sea-level
        penalty = 0.03 * min(1.0, pr - 1.0)
    else:
        # Underexpanded in high altitude / vacuum
        penalty = 0.02 * (1.0 - pr)

    return max(0.85, min(0.99, base_efficiency - penalty))


@dataclass
class RotatingDetonationValidationResult:
    """Structured validation report for Rotating Detonation Rocket Engine parameters."""
    is_valid: bool
    cj_detonation_velocity_m_s: float
    cj_pressure_ratio: float
    znd_spike_pressure_ratio: float
    ddt_runup_distance_mm: float
    detonation_frequency_khz: float
    num_co_rotating_waves: int
    annular_channel_gap_mm: float
    annular_diameter_mm: float
    pressure_gain_efficiency: float
    aerospike_nozzle_efficiency: float
    specific_impulse_s: float
    chamber_wall_heat_flux_mw_m2: float
    flaws: List[str]


def validate_rotating_detonation_parameters(
    cj_detonation_velocity_m_s: float = 2780.0,
    cj_pressure_ratio: float = 22.4,
    znd_spike_pressure_ratio: float = 42.0,
    ddt_runup_distance_mm: float = 8.5,
    detonation_frequency_khz: float = 28.5,
    num_co_rotating_waves: int = 2,
    annular_channel_gap_mm: float = 5.2,
    annular_diameter_mm: float = 120.0,
    pressure_gain_efficiency: float = 0.18,
    aerospike_nozzle_efficiency: float = 0.94,
    specific_impulse_s: float = 465.0,
    chamber_wall_heat_flux_mw_m2: float = 24.5
) -> RotatingDetonationValidationResult:
    """Validate rotating detonation rocket engine parameters against Commander Jaxen Sterling's benchmarks."""
    flaws: List[str] = []

    if cj_detonation_velocity_m_s < MIN_CJ_DETONATION_VELOCITY_M_S:
        flaws.append(
            f"Chapman-Jouguet detonation velocity {cj_detonation_velocity_m_s:.1f} m/s below supersonic threshold "
            f"{MIN_CJ_DETONATION_VELOCITY_M_S:.1f} m/s (risk of deflagration flame blowout)."
        )

    if cj_pressure_ratio < MIN_CJ_PRESSURE_RATIO:
        flaws.append(
            f"CJ detonation pressure ratio {cj_pressure_ratio:.1f} below minimum threshold "
            f"{MIN_CJ_PRESSURE_RATIO:.1f}."
        )

    if znd_spike_pressure_ratio < MIN_ZND_SPIKE_PRESSURE_RATIO:
        flaws.append(
            f"ZND leading shock spike pressure ratio {znd_spike_pressure_ratio:.1f} below minimum "
            f"{MIN_ZND_SPIKE_PRESSURE_RATIO:.1f}."
        )

    if ddt_runup_distance_mm > MAX_DDT_RUNUP_DISTANCE_MM:
        flaws.append(
            f"DDT run-up transition distance {ddt_runup_distance_mm:.1f} mm exceeds maximum threshold "
            f"{MAX_DDT_RUNUP_DISTANCE_MM:.1f} mm (parasitic deflagration risk)."
        )

    if detonation_frequency_khz < MIN_DETONATION_FREQUENCY_KHZ:
        flaws.append(
            f"Rotating wave frequency {detonation_frequency_khz:.1f} kHz below stability floor "
            f"{MIN_DETONATION_FREQUENCY_KHZ:.1f} kHz."
        )

    if num_co_rotating_waves < MIN_CO_ROTATING_WAVES:
        flaws.append(
            f"Number of co-rotating wave heads {num_co_rotating_waves} below minimum {MIN_CO_ROTATING_WAVES}."
        )

    if annular_channel_gap_mm < MIN_ANNULAR_GAP_MM or annular_channel_gap_mm > MAX_ANNULAR_GAP_MM:
        flaws.append(
            f"Annular channel gap {annular_channel_gap_mm:.2f} mm outside allowable range "
            f"[{MIN_ANNULAR_GAP_MM:.1f}, {MAX_ANNULAR_GAP_MM:.1f}] mm."
        )

    if annular_diameter_mm < MIN_ANNULAR_DIAMETER_MM or annular_diameter_mm > MAX_ANNULAR_DIAMETER_MM:
        flaws.append(
            f"Annular chamber diameter {annular_diameter_mm:.1f} mm outside allowable bounds "
            f"[{MIN_ANNULAR_DIAMETER_MM:.1f}, {MAX_ANNULAR_DIAMETER_MM:.1f}] mm."
        )

    if pressure_gain_efficiency < MIN_PRESSURE_GAIN_EFFICIENCY:
        flaws.append(
            f"Thermodynamic pressure gain efficiency {pressure_gain_efficiency:.3f} below minimum "
            f"{MIN_PRESSURE_GAIN_EFFICIENCY:.2f}."
        )

    if aerospike_nozzle_efficiency < MIN_AEROSPIKE_NOZZLE_EFFICIENCY:
        flaws.append(
            f"Aerospike plug expansion nozzle efficiency {aerospike_nozzle_efficiency:.3f} below benchmark "
            f"{MIN_AEROSPIKE_NOZZLE_EFFICIENCY:.2f}."
        )

    if specific_impulse_s < MIN_SPECIFIC_IMPULSE_S:
        flaws.append(
            f"Specific impulse {specific_impulse_s:.1f} s below performance benchmark {MIN_SPECIFIC_IMPULSE_S:.1f} s."
        )

    if chamber_wall_heat_flux_mw_m2 > MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2:
        flaws.append(
            f"Chamber wall heat flux {chamber_wall_heat_flux_mw_m2:.1f} MW/m^2 exceeds regenerative cooling ceiling "
            f"{MAX_CHAMBER_WALL_HEAT_FLUX_MW_M2:.1f} MW/m^2."
        )

    return RotatingDetonationValidationResult(
        is_valid=len(flaws) == 0,
        cj_detonation_velocity_m_s=cj_detonation_velocity_m_s,
        cj_pressure_ratio=cj_pressure_ratio,
        znd_spike_pressure_ratio=znd_spike_pressure_ratio,
        ddt_runup_distance_mm=ddt_runup_distance_mm,
        detonation_frequency_khz=detonation_frequency_khz,
        num_co_rotating_waves=num_co_rotating_waves,
        annular_channel_gap_mm=annular_channel_gap_mm,
        annular_diameter_mm=annular_diameter_mm,
        pressure_gain_efficiency=pressure_gain_efficiency,
        aerospike_nozzle_efficiency=aerospike_nozzle_efficiency,
        specific_impulse_s=specific_impulse_s,
        chamber_wall_heat_flux_mw_m2=chamber_wall_heat_flux_mw_m2,
        flaws=flaws
    )
