"""Physical references and mathematical models for Magnetospheric Radiation Shielding & Particle Deflection.

Architect: Commander Kaelen 'The Shield' Vance
Domain: magnetospheric_radiation_shielding_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Fundamental physical constants
SPEED_OF_LIGHT: float = 299792458.0           # m/s
VACUUM_PERMEABILITY: float = 4.0 * math.pi * 1.0e-7  # H/m (T*m/A)
ELEMENTARY_CHARGE: float = 1.602176634e-19    # C
PROTON_REST_MASS_KG: float = 1.67262192369e-27  # kg
PROTON_REST_ENERGY_MEV: float = 938.272       # MeV

# Standard engineering bounds for active magnetospheric shielding
MIN_MAGNETIC_MOMENT_GA_M2: float = 10.0       # 10.0 GA*m^2 (1.0e10 A*m^2)
MIN_STORMER_RIGIDITY_GV: float = 5.0          # 5.0 GV cut-off
MIN_COIL_PEAK_FIELD_T: float = 4.0            # 4.0 Tesla
MAX_HABITAT_LEAKAGE_FIELD_T: float = 5.0e-4   # 0.50 mT (5.0 Gauss)
MIN_HTS_CURRENT_DENSITY_A_M2: float = 5.0e8   # 500.0 A/mm^2 (5.0e8 A/m^2)
MAX_COIL_OPERATING_TEMP_K: float = 25.0       # 25.0 K
MAX_QUENCH_DUMP_TIME_MS: float = 100.0        # 100.0 ms
MAX_CREW_ANNUAL_DOSE_MSV: float = 100.0       # 100.0 mSv/year (0.10 Sv/year)
MAX_SPE_DOSE_RATE_MGY_H: float = 25.0         # 25.0 mGy/h
MIN_ELECTROSTATIC_POTENTIAL_MV: float = 2.0   # 2.0 MV
MIN_NEUTRALIZER_CURRENT_MA: float = 50.0      # 50.0 mA
NOMINAL_BUCKING_ATTENUATION: float = 1.0e-3   # 99.9% active bucking coil cancellation


def calculate_stormer_cutoff_rigidity(
    magnetic_moment_a_m2: float,
    radius_m: float
) -> float:
    """Calculate Stormer magnetic cut-off rigidity in Gigavolts (GV).

    R_c = (mu_0 * c * M) / (4 * pi * r^2 * 10^9)  [GV]
    """
    if magnetic_moment_a_m2 <= 0.0 or radius_m <= 0.0:
        return 0.0
    rigidity_volts = (VACUUM_PERMEABILITY * SPEED_OF_LIGHT * magnetic_moment_a_m2) / (4.0 * math.pi * (radius_m ** 2))
    return rigidity_volts / 1.0e9  # Convert to GV


def calculate_larmor_gyroradius(
    kinetic_energy_mev: float,
    magnetic_field_t: float
) -> float:
    """Calculate relativistic gyroradius (Larmor radius) of proton in meters.

    E_total = E_k + m_p * c^2
    p = sqrt(E_total^2 - E_rest^2) / c
    r_L = p / (q * B)
    """
    if kinetic_energy_mev <= 0.0 or magnetic_field_t <= 0.0:
        return float("inf")

    e_total_mev = kinetic_energy_mev + PROTON_REST_ENERGY_MEV
    momentum_mev_c = math.sqrt((e_total_mev ** 2) - (PROTON_REST_ENERGY_MEV ** 2))
    momentum_kg_m_s = (momentum_mev_c * 1.0e6 * ELEMENTARY_CHARGE) / SPEED_OF_LIGHT
    return momentum_kg_m_s / (ELEMENTARY_CHARGE * magnetic_field_t)


def calculate_habitat_fringe_field(
    magnetic_moment_a_m2: float,
    distance_m: float,
    bucking_attenuation_ratio: float = NOMINAL_BUCKING_ATTENUATION
) -> float:
    """Calculate compensated magnetic flux density in Tesla inside crew habitat using bucking coils.

    B_net = B_unshielded * bucking_attenuation_ratio
    B_unshielded = (mu_0 * M) / (4 * pi * r^3)
    """
    if magnetic_moment_a_m2 <= 0.0 or distance_m <= 0.0:
        return 0.0
    b_unshielded = (VACUUM_PERMEABILITY * magnetic_moment_a_m2) / (4.0 * math.pi * (distance_m ** 3))
    return b_unshielded * max(0.0, bucking_attenuation_ratio)


@dataclass
class MagnetosphericShieldValidationResult:
    """Structured validation report for Active Magnetospheric Radiation Shielding."""
    is_valid: bool
    magnetic_moment_ga_m2: float
    stormer_rigidity_gv: float
    coil_peak_field_t: float
    habitat_leakage_field_mt: float
    hts_current_density_a_mm2: float
    coil_operating_temp_k: float
    quench_dump_time_ms: float
    crew_annual_dose_msv: float
    spe_dose_rate_mgy_h: float
    electrostatic_potential_mv: float
    neutralizer_current_ma: float
    flaws: List[str]


def validate_magnetospheric_shield_parameters(
    magnetic_moment_ga_m2: float = 45.0,
    stormer_rigidity_gv: float = 6.8,
    coil_peak_field_t: float = 5.5,
    habitat_leakage_field_mt: float = 0.35,
    hts_current_density_a_mm2: float = 650.0,
    coil_operating_temp_k: float = 20.0,
    quench_dump_time_ms: float = 65.0,
    crew_annual_dose_msv: float = 45.0,
    spe_dose_rate_mgy_h: float = 12.0,
    electrostatic_potential_mv: float = 2.5,
    neutralizer_current_ma: float = 75.0
) -> MagnetosphericShieldValidationResult:
    """Validate active magnetospheric shield parameters against Commander Kaelen Vance's strict radiation benchmarks."""
    flaws: List[str] = []

    if magnetic_moment_ga_m2 < MIN_MAGNETIC_MOMENT_GA_M2:
        flaws.append(
            f"Magnetic dipole moment {magnetic_moment_ga_m2:.1f} GA*m^2 below threshold {MIN_MAGNETIC_MOMENT_GA_M2:.1f} GA*m^2."
        )

    if stormer_rigidity_gv < MIN_STORMER_RIGIDITY_GV:
        flaws.append(
            f"Stormer cut-off rigidity {stormer_rigidity_gv:.2f} GV below minimum deflection bound {MIN_STORMER_RIGIDITY_GV:.2f} GV."
        )

    if coil_peak_field_t < MIN_COIL_PEAK_FIELD_T:
        flaws.append(
            f"Coil peak magnetic field {coil_peak_field_t:.1f} T below required deflection intensity {MIN_COIL_PEAK_FIELD_T:.1f} T."
        )

    if habitat_leakage_field_mt > (MAX_HABITAT_LEAKAGE_FIELD_T * 1000.0):
        flaws.append(
            f"Habitat magnetic fringe field {habitat_leakage_field_mt:.2f} mT exceeds human safety limit {MAX_HABITAT_LEAKAGE_FIELD_T * 1000.0:.2f} mT (5.0 Gauss)."
        )

    if hts_current_density_a_mm2 < (MIN_HTS_CURRENT_DENSITY_A_M2 / 1.0e6):
        flaws.append(
            f"HTS REBCO critical current density {hts_current_density_a_mm2:.1f} A/mm^2 below benchmark {MIN_HTS_CURRENT_DENSITY_A_M2 / 1.0e6:.1f} A/mm^2."
        )

    if coil_operating_temp_k > MAX_COIL_OPERATING_TEMP_K:
        flaws.append(
            f"Superconducting coil operating temperature {coil_operating_temp_k:.1f} K exceeds cryogenic ceiling {MAX_COIL_OPERATING_TEMP_K:.1f} K."
        )

    if quench_dump_time_ms > MAX_QUENCH_DUMP_TIME_MS:
        flaws.append(
            f"Quench energy dump extraction time {quench_dump_time_ms:.1f} ms exceeds safety limit {MAX_QUENCH_DUMP_TIME_MS:.1f} ms."
        )

    if crew_annual_dose_msv > MAX_CREW_ANNUAL_DOSE_MSV:
        flaws.append(
            f"Crew annual effective dose {crew_annual_dose_msv:.1f} mSv/year exceeds ALARA ceiling {MAX_CREW_ANNUAL_DOSE_MSV:.1f} mSv/year."
        )

    if spe_dose_rate_mgy_h > MAX_SPE_DOSE_RATE_MGY_H:
        flaws.append(
            f"Acute SPE dose rate {spe_dose_rate_mgy_h:.1f} mGy/h exceeds acute radiation syndrome bound {MAX_SPE_DOSE_RATE_MGY_H:.1f} mGy/h."
        )

    if electrostatic_potential_mv < MIN_ELECTROSTATIC_POTENTIAL_MV:
        flaws.append(
            f"Electrostatic grid potential {electrostatic_potential_mv:.1f} MV below repulsive threshold {MIN_ELECTROSTATIC_POTENTIAL_MV:.1f} MV."
        )

    if neutralizer_current_ma < MIN_NEUTRALIZER_CURRENT_MA:
        flaws.append(
            f"Space charge neutralizer current {neutralizer_current_ma:.1f} mA below solar wind compensation requirement {MIN_NEUTRALIZER_CURRENT_MA:.1f} mA."
        )

    return MagnetosphericShieldValidationResult(
        is_valid=len(flaws) == 0,
        magnetic_moment_ga_m2=magnetic_moment_ga_m2,
        stormer_rigidity_gv=stormer_rigidity_gv,
        coil_peak_field_t=coil_peak_field_t,
        habitat_leakage_field_mt=habitat_leakage_field_mt,
        hts_current_density_a_mm2=hts_current_density_a_mm2,
        coil_operating_temp_k=coil_operating_temp_k,
        quench_dump_time_ms=quench_dump_time_ms,
        crew_annual_dose_msv=crew_annual_dose_msv,
        spe_dose_rate_mgy_h=spe_dose_rate_mgy_h,
        electrostatic_potential_mv=electrostatic_potential_mv,
        neutralizer_current_ma=neutralizer_current_ma,
        flaws=flaws
    )
