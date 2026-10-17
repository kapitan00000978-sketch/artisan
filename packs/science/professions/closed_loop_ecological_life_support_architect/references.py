"""Physical references and mathematical models for Closed-Loop ECLSS & Bioregenerative Space Architecture.

Architect: Dr. Morwenna 'The Biosphere' Sterling
Domain: closed_loop_ecological_life_support_architect
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Physical constants and molar masses (kg/mol)
MOLAR_MASS_CO2: float = 0.04401      # kg/mol
MOLAR_MASS_H2: float = 0.002016      # kg/mol
MOLAR_MASS_H2O: float = 0.018015     # kg/mol
MOLAR_MASS_O2: float = 0.0319988     # kg/mol
MOLAR_MASS_CH4: float = 0.016043     # kg/mol

# Stoichiometric coefficients for Sabatier: CO2 + 4 H2 -> CH4 + 2 H2O
SABATIER_H2O_RATIO: float = (2.0 * MOLAR_MASS_H2O) / MOLAR_MASS_CO2    # ~0.8187 kg H2O / kg CO2
SABATIER_CH4_RATIO: float = MOLAR_MASS_CH4 / MOLAR_MASS_CO2            # ~0.3645 kg CH4 / kg CO2
SABATIER_H2_REQ_RATIO: float = (4.0 * MOLAR_MASS_H2) / MOLAR_MASS_CO2  # ~0.1832 kg H2 / kg CO2

# Electrolysis ratios: 2 H2O -> 2 H2 + O2
ELECTROLYSIS_O2_RATIO: float = MOLAR_MASS_O2 / (2.0 * MOLAR_MASS_H2O)  # ~0.8881 kg O2 / kg H2O
ELECTROLYSIS_H2_RATIO: float = (2.0 * MOLAR_MASS_H2) / (2.0 * MOLAR_MASS_H2O) # ~0.1119 kg H2 / kg H2O

# Standard physical & operational boundaries
MIN_SABATIER_EFFICIENCY: float = 0.85          # 85.0%
MIN_ELECTROLYSIS_EFFICIENCY: float = 0.80      # 80.0%
MIN_WATER_LOOP_RECOVERY: float = 0.98          # 98.0%
MAX_PERMEATE_TOC_UG_PER_L: float = 500.0       # 500 ug/L (0.50 mg/L)
MIN_O2_CONSUMPTION_KG_DAY: float = 0.80        # kg/day/crew
MAX_O2_CONSUMPTION_KG_DAY: float = 0.90        # kg/day/crew
MIN_CO2_PRODUCTION_KG_DAY: float = 0.95        # kg/day/crew
MAX_CO2_PRODUCTION_KG_DAY: float = 1.05        # kg/day/crew
MIN_PQ_RATIO: float = 1.05                     # Photosynthetic Quotient min
MAX_PQ_RATIO: float = 1.25                     # Photosynthetic Quotient max
NOMINAL_PQ_RATIO: float = 1.15                 # Photosynthetic Quotient nominal
MIN_BIOMASS_GROWTH_RATE_HR: float = 0.05       # 0.05 h^-1
MIN_PAR_PPFD_UMOL_M2_S: float = 200.0          # 200 umol/m^2/s
MIN_CABIN_TOTAL_PRESSURE_KPA: float = 70.0     # 70.0 kPa
MAX_CABIN_TOTAL_PRESSURE_KPA: float = 101.3    # 101.3 kPa (1 atm)
MIN_CABIN_PO2_KPA: float = 19.5                # 19.5 kPa
MAX_CABIN_PO2_KPA: float = 23.5                # 23.5 kPa
MAX_CABIN_PCO2_KPA: float = 0.40               # 0.40 kPa (3.0 mmHg)
MIN_CATALYTIC_OXIDIZER_TEMP_C: float = 400.0   # 400.0 C


def calculate_sabatier_yield(
    m_co2_kg: float,
    efficiency: float = 0.85
) -> Tuple[float, float, float]:
    """Calculate water produced, methane produced, and hydrogen required for Sabatier reduction.

    CO2 + 4 H2 -> CH4 + 2 H2O.
    Returns: (water_produced_kg, methane_produced_kg, hydrogen_required_kg)
    """
    if m_co2_kg <= 0.0 or efficiency <= 0.0:
        return 0.0, 0.0, 0.0
    eff = min(1.0, efficiency)
    m_h2o = m_co2_kg * eff * SABATIER_H2O_RATIO
    m_ch4 = m_co2_kg * eff * SABATIER_CH4_RATIO
    m_h2_req = m_co2_kg * eff * SABATIER_H2_REQ_RATIO
    return m_h2o, m_ch4, m_h2_req


def calculate_electrolysis_yield(
    m_water_kg: float,
    efficiency: float = 0.80
) -> Tuple[float, float]:
    """Calculate oxygen and hydrogen yields from PEM water electrolysis.

    2 H2O -> 2 H2 + O2.
    Returns: (o2_yield_kg, h2_yield_kg)
    """
    if m_water_kg <= 0.0 or efficiency <= 0.0:
        return 0.0, 0.0
    eff = min(1.0, efficiency)
    m_o2 = m_water_kg * eff * ELECTROLYSIS_O2_RATIO
    m_h2 = m_water_kg * eff * ELECTROLYSIS_H2_RATIO
    return m_o2, m_h2


def calculate_photobioreactor_o2_output(
    co2_uptake_kg: float,
    photosynthetic_quotient: float = NOMINAL_PQ_RATIO
) -> float:
    """Calculate oxygen mass generated from photosynthetic microalgae given CO2 uptake.

    PQ = mol O2 / mol CO2.
    """
    if co2_uptake_kg <= 0.0 or photosynthetic_quotient <= 0.0:
        return 0.0
    moles_co2 = co2_uptake_kg / MOLAR_MASS_CO2
    moles_o2 = moles_co2 * photosynthetic_quotient
    return moles_o2 * MOLAR_MASS_O2


def calculate_water_recovery_balance(
    graywater_in_l: float,
    recovery_fraction: float = MIN_WATER_LOOP_RECOVERY
) -> Tuple[float, float]:
    """Calculate potable water recovered and concentrated brine residue from distillation.

    Returns: (potable_recovered_l, brine_waste_l)
    """
    if graywater_in_l <= 0.0:
        return 0.0, 0.0
    rec = max(0.0, min(1.0, recovery_fraction))
    potable = graywater_in_l * rec
    brine = graywater_in_l * (1.0 - rec)
    return potable, brine


@dataclass
class ECLSSValidationResult:
    """Structured validation report for Closed-Loop ECLSS and Bioregenerative Architecture."""
    is_valid: bool
    sabatier_efficiency: float
    electrolysis_efficiency: float
    water_recovery_fraction: float
    permeate_toc_ug_per_l: float
    crew_o2_rate_kg_day: float
    crew_co2_rate_kg_day: float
    photosynthetic_quotient: float
    algal_growth_rate_hr: float
    cabin_pressure_kpa: float
    cabin_po2_kpa: float
    cabin_pco2_kpa: float
    catalytic_temp_c: float
    flaws: List[str]


def validate_eclss_parameters(
    sabatier_efficiency: float = 0.88,
    electrolysis_efficiency: float = 0.85,
    water_recovery_fraction: float = 0.985,
    permeate_toc_ug_per_l: float = 350.0,
    crew_o2_rate_kg_day: float = 0.84,
    crew_co2_rate_kg_day: float = 1.00,
    photosynthetic_quotient: float = 1.15,
    algal_growth_rate_hr: float = 0.065,
    cabin_pressure_kpa: float = 101.3,
    cabin_po2_kpa: float = 21.0,
    cabin_pco2_kpa: float = 0.30,
    catalytic_temp_c: float = 425.0
) -> ECLSSValidationResult:
    """Validate closed-loop ECLSS parameters against Dr. Morwenna Sterling's strict physical benchmarks."""
    flaws: List[str] = []

    if sabatier_efficiency < MIN_SABATIER_EFFICIENCY:
        flaws.append(
            f"Sabatier conversion efficiency {sabatier_efficiency:.3f} below minimum {MIN_SABATIER_EFFICIENCY:.3f}."
        )

    if electrolysis_efficiency < MIN_ELECTROLYSIS_EFFICIENCY:
        flaws.append(
            f"PEM water electrolysis efficiency {electrolysis_efficiency:.3f} below minimum {MIN_ELECTROLYSIS_EFFICIENCY:.3f}."
        )

    if water_recovery_fraction < MIN_WATER_LOOP_RECOVERY:
        flaws.append(
            f"Water loop recovery fraction {water_recovery_fraction:.3f} below minimum {MIN_WATER_LOOP_RECOVERY:.3f} (98.0%)."
        )

    if permeate_toc_ug_per_l > MAX_PERMEATE_TOC_UG_PER_L:
        flaws.append(
            f"Permeate TOC {permeate_toc_ug_per_l:.1f} ug/L exceeds maximum allowable {MAX_PERMEATE_TOC_UG_PER_L:.1f} ug/L."
        )

    if not (MIN_O2_CONSUMPTION_KG_DAY <= crew_o2_rate_kg_day <= MAX_O2_CONSUMPTION_KG_DAY):
        flaws.append(
            f"Metabolic O2 consumption {crew_o2_rate_kg_day:.2f} kg/day/crew outside physiological band [{MIN_O2_CONSUMPTION_KG_DAY}, {MAX_O2_CONSUMPTION_KG_DAY}]."
        )

    if not (MIN_CO2_PRODUCTION_KG_DAY <= crew_co2_rate_kg_day <= MAX_CO2_PRODUCTION_KG_DAY):
        flaws.append(
            f"Metabolic CO2 generation {crew_co2_rate_kg_day:.2f} kg/day/crew outside physiological band [{MIN_CO2_PRODUCTION_KG_DAY}, {MAX_CO2_PRODUCTION_KG_DAY}]."
        )

    if not (MIN_PQ_RATIO <= photosynthetic_quotient <= MAX_PQ_RATIO):
        flaws.append(
            f"Photosynthetic Quotient {photosynthetic_quotient:.2f} outside photobioreactor bounds [{MIN_PQ_RATIO}, {MAX_PQ_RATIO}]."
        )

    if algal_growth_rate_hr < MIN_BIOMASS_GROWTH_RATE_HR:
        flaws.append(
            f"Algal biomass growth rate {algal_growth_rate_hr:.3f} h^-1 below threshold {MIN_BIOMASS_GROWTH_RATE_HR:.3f} h^-1."
        )

    if not (MIN_CABIN_TOTAL_PRESSURE_KPA <= cabin_pressure_kpa <= MAX_CABIN_TOTAL_PRESSURE_KPA):
        flaws.append(
            f"Cabin pressure {cabin_pressure_kpa:.1f} kPa outside safe operational range [{MIN_CABIN_TOTAL_PRESSURE_KPA}, {MAX_CABIN_TOTAL_PRESSURE_KPA}]."
        )

    if not (MIN_CABIN_PO2_KPA <= cabin_po2_kpa <= MAX_CABIN_PO2_KPA):
        flaws.append(
            f"Cabin pO2 {cabin_po2_kpa:.1f} kPa violates physiological hypoxia/hyperoxia limits [{MIN_CABIN_PO2_KPA}, {MAX_CABIN_PO2_KPA}]."
        )

    if cabin_pco2_kpa > MAX_CABIN_PCO2_KPA:
        flaws.append(
            f"Cabin pCO2 {cabin_pco2_kpa:.2f} kPa exceeds hypercapnia limit {MAX_CABIN_PCO2_KPA:.2f} kPa (3.0 mmHg)."
        )

    if catalytic_temp_c < MIN_CATALYTIC_OXIDIZER_TEMP_C:
        flaws.append(
            f"Catalytic oxidizer temperature {catalytic_temp_c:.1f} C below VOC cracking threshold {MIN_CATALYTIC_OXIDIZER_TEMP_C:.1f} C."
        )

    return ECLSSValidationResult(
        is_valid=len(flaws) == 0,
        sabatier_efficiency=sabatier_efficiency,
        electrolysis_efficiency=electrolysis_efficiency,
        water_recovery_fraction=water_recovery_fraction,
        permeate_toc_ug_per_l=permeate_toc_ug_per_l,
        crew_o2_rate_kg_day=crew_o2_rate_kg_day,
        crew_co2_rate_kg_day=crew_co2_rate_kg_day,
        photosynthetic_quotient=photosynthetic_quotient,
        algal_growth_rate_hr=algal_growth_rate_hr,
        cabin_pressure_kpa=cabin_pressure_kpa,
        cabin_po2_kpa=cabin_po2_kpa,
        cabin_pco2_kpa=cabin_pco2_kpa,
        catalytic_temp_c=catalytic_temp_c,
        flaws=flaws
    )
