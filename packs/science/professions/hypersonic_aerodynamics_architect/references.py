"""Empirical references and physical constants for Hypersonic Aerothermodynamics & Scramjet Propulsion.

Maintained by Dr. Zephyr 'The Hypersonic' Sterling.
Enforces non-equilibrium real-gas high-temperature thermodynamics,
Sutton-Graves stagnation aerothermal heating, scramjet isolator unstart defense,
and Ultra-High-Temperature Ceramic (UHTC) thermal protection envelopes.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# Standard physical constants
UNIVERSAL_GAS_CONSTANT: float = 8314.46  # J / (kmol * K)
AIR_GAS_CONSTANT: float = 287.05         # J / (kg * K)
STANDARD_SEA_LEVEL_TEMP_K: float = 288.15
STANDARD_SEA_LEVEL_PRESSURE_PA: float = 101325.0
STANDARD_SEA_LEVEL_DENSITY: float = 1.225  # kg / m^3

# Sutton-Graves constant for Earth air atmosphere (kg^0.5 / m)
SUTTON_GRAVES_CONSTANT: float = 1.7415e-4


@dataclass(frozen=True)
class HypersonicFreestreamState:
    """Freestream atmospheric flight conditions in the hypersonic regime."""
    mach_number: float
    altitude_m: float
    velocity_mps: float
    ambient_temperature_k: float
    ambient_pressure_pa: float
    density_kg_m3: float

    def is_hypersonic_regime(self) -> bool:
        """Verify Mach number is within the true hypersonic regime (Mach 5.0 to 25.0)."""
        return 5.0 <= self.mach_number <= 25.0


@dataclass(frozen=True)
class ShockLayerThermodynamics:
    """Non-equilibrium gas dynamics and molecular dissociation parameters across shock."""
    stagnation_temperature_k: float
    post_shock_temperature_k: float
    dissociation_fraction_o2: float
    dissociation_fraction_n2: float
    is_real_gas_active: bool
    specific_heat_ratio_effective: float

    def is_real_gas_valid(self) -> bool:
        """Ensure real-gas chemistry is engaged when shock temperature exceeds 2000 K."""
        if self.post_shock_temperature_k >= 2000.0:
            return (
                self.is_real_gas_active and
                self.dissociation_fraction_o2 > 0.0 and
                self.specific_heat_ratio_effective < 1.40
            )
        return True


@dataclass(frozen=True)
class ScramjetIsolatorState:
    """Scramjet isolator shock train dynamics and unstart prevention margins."""
    isolator_length_m: float
    isolator_height_m: float
    shock_train_length_m: float
    combustor_to_inlet_pressure_ratio: float
    isolator_stability_margin: float
    response_time_ms: float
    is_unstart_imminent: bool

    def is_isolator_stable(self) -> bool:
        """Verify isolator shock train stability margin >= 1.25 and sub-5ms unstart response."""
        return (
            self.isolator_stability_margin >= 1.25 and
            self.response_time_ms <= 5.0 and
            not self.is_unstart_imminent
        )


@dataclass(frozen=True)
class ThermalProtectionState:
    """Thermal Protection System (TPS) aerothermal heat flux and material limits."""
    peak_heat_flux_mw_m2: float
    nose_radius_m: float
    surface_temperature_k: float
    material_limit_temperature_k: float
    tps_safety_factor: float

    def is_tps_safe(self) -> bool:
        """Verify TPS safety margin >= 1.50 and surface temp below material oxidation limit."""
        return (
            self.tps_safety_factor >= 1.50 and
            self.surface_temperature_k <= self.material_limit_temperature_k and
            self.surface_temperature_k <= 2500.0
        )


@dataclass
class HypersonicMissionReport:
    """Comprehensive hypersonic flight envelope and aerothermodynamic audit report."""
    mission_id: str
    aerothermal_valid: bool
    scramjet_stable: bool
    tps_safe: bool
    real_gas_modeled: bool
    safety_score: float
    anomalies: List[str] = field(default_factory=list)
    summary: str = ""


def calculate_stagnation_temperature(ambient_temp_k: float, mach: float, gamma: float = 1.4) -> float:
    """Calculate ideal total stagnation temperature in Kelvin.
    T0 = T_inf * (1 + (gamma - 1) / 2 * M^2)
    """
    if mach < 0.0 or ambient_temp_k <= 0.0:
        raise ValueError("Mach and temperature must be positive.")
    return ambient_temp_k * (1.0 + ((gamma - 1.0) / 2.0) * (mach ** 2))


def calculate_sutton_graves_heat_flux(
    density_kg_m3: float,
    velocity_mps: float,
    nose_radius_m: float,
    k_sg: float = SUTTON_GRAVES_CONSTANT
) -> float:
    """Calculate stagnation point aerothermal heat flux using the Sutton-Graves formula.
    q_stag = k_sg * sqrt(rho / R_n) * V^3 (W/m^2)
    Returns heat flux in MW/m^2.
    """
    if nose_radius_m <= 0.0 or density_kg_m3 <= 0.0 or velocity_mps <= 0.0:
        raise ValueError("Radius, density, and velocity must be strictly positive.")
    q_watts = k_sg * math.sqrt(density_kg_m3 / nose_radius_m) * (velocity_mps ** 3)
    return q_watts * 1e-6  # Convert W/m^2 to MW/m^2


def calculate_isolator_shock_train_length(
    isolator_height_m: float,
    pressure_ratio_combustor_to_inlet: float
) -> float:
    """Calculate pre-combustion shock train length in scramjet isolator using Waltrup & Billig relation.
    L_st = H * 1.4 * (P_comb / P_inlet - 1.0)
    """
    if isolator_height_m <= 0.0 or pressure_ratio_combustor_to_inlet < 1.0:
        raise ValueError("Height must be positive and pressure ratio >= 1.0.")
    return isolator_height_m * 1.4 * (pressure_ratio_combustor_to_inlet - 1.0)


def evaluate_isolator_stability_margin(
    isolator_length_m: float,
    shock_train_length_m: float
) -> float:
    """Evaluate scramjet isolator margin against unstart.
    Margin = L_isolator / L_shock_train
    """
    if shock_train_length_m <= 0.0:
        return float("inf")
    return isolator_length_m / shock_train_length_m


def evaluate_tps_safety_factor(
    material_flux_limit_mw_m2: float,
    actual_peak_flux_mw_m2: float
) -> float:
    """Evaluate Thermal Protection System (TPS) heat flux safety factor."""
    if actual_peak_flux_mw_m2 <= 0.0:
        raise ValueError("Actual heat flux must be strictly positive.")
    return material_flux_limit_mw_m2 / actual_peak_flux_mw_m2


class HypersonicReferenceLibrary:
    """Empirical bounds and canonical reference implementation for Hypersonic Aerothermodynamics."""

    MIN_HYPERSONIC_MACH: float = 5.0
    MAX_HYPERSONIC_MACH: float = 25.0
    MIN_ISOLATOR_MARGIN: float = 1.25
    MIN_TPS_SAFETY_FACTOR: float = 1.50
    MAX_UHTC_TEMPERATURE_K: float = 2500.0
    MAX_UNSTART_RESPONSE_MS: float = 5.0
    MIN_SENSOR_FREQUENCY_KHZ: float = 50.0

    @classmethod
    def get_canonical_core(cls) -> str:
        """Returns reference production-grade implementation for hypersonic scramjet executive."""
        return r'''"""Canonical Hypersonic Aerothermodynamics & Scramjet Autonomy Core.
Authored to the strict physical benchmarks of Dr. Zephyr Sterling.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class HypersonicFlightTelemetry:
    mach_number: float
    altitude_m: float
    velocity_mps: float
    density_kg_m3: float
    ambient_temp_k: float
    nose_radius_m: float
    isolator_length_m: float
    isolator_height_m: float
    combustor_pressure_ratio: float
    tps_material_flux_limit_mw_m2: float
    unstart_actuator_latency_ms: float


class HypersonicAutonomyExecutive:
    """Deterministic executive managing hypersonic flight envelopes and scramjet stability."""

    def __init__(self) -> None:
        self.min_mach = 5.0
        self.max_mach = 25.0
        self.min_isolator_margin = 1.25
        self.min_tps_safety_factor = 1.50
        self.max_uhtc_temp_k = 2500.0
        self.is_emergency_scram_active = False
        self.abort_reason: Optional[str] = None

    def calculate_stagnation_aerothermal_heating(
        self,
        density_kg_m3: float,
        velocity_mps: float,
        nose_radius_m: float
    ) -> float:
        """Compute Sutton-Graves stagnation heat flux in MW/m^2."""
        k_sg = 1.7415e-4
        q_watts = k_sg * math.sqrt(density_kg_m3 / max(nose_radius_m, 1e-4)) * (velocity_mps ** 3)
        return q_watts * 1e-6

    def evaluate_real_gas_shock_temperature(self, t_inf_k: float, mach: float) -> Tuple[float, bool]:
        """Compute stagnation temperature with high-temperature dissociation damping."""
        ideal_t0 = t_inf_k * (1.0 + 0.2 * (mach ** 2))
        is_real_gas = ideal_t0 >= 2000.0
        if is_real_gas:
            # Enthalpy sinks into molecular O2/N2 dissociation (approx 20% damping)
            actual_t0 = 2000.0 + (ideal_t0 - 2000.0) * 0.78
        else:
            actual_t0 = ideal_t0
        return (actual_t0, is_real_gas)

    def evaluate_scramjet_isolator_stability(
        self,
        isolator_length_m: float,
        isolator_height_m: float,
        pressure_ratio: float
    ) -> Tuple[float, float, bool]:
        """Evaluate Waltrup-Billig shock train length and isolator stability margin."""
        shock_train_length = isolator_height_m * 1.4 * max(0.0, pressure_ratio - 1.0)
        margin = isolator_length_m / max(shock_train_length, 1e-3)
        is_stable = margin >= self.min_isolator_margin
        return (shock_train_length, margin, is_stable)

    def evaluate_telemetry_safety(self, telem: HypersonicFlightTelemetry) -> Tuple[bool, List[str]]:
        """Ruthlessly audit hypersonic flight telemetry against aerothermodynamic invariants."""
        anomalies: List[str] = []

        # 1. Hypersonic regime check
        if not (self.min_mach <= telem.mach_number <= self.max_mach):
            anomalies.append(f"Mach {telem.mach_number:.2f} is outside hypersonic envelope [5.0, 25.0]")

        # 2. Aerothermal stagnation heat flux & TPS safety factor
        q_stag = self.calculate_stagnation_aerothermal_heating(
            telem.density_kg_m3, telem.velocity_mps, telem.nose_radius_m
        )
        tps_sf = telem.tps_material_flux_limit_mw_m2 / max(q_stag, 1e-3)
        if tps_sf < self.min_tps_safety_factor:
            anomalies.append(f"TPS safety factor below 1.50 (SF={tps_sf:.2f}, q_stag={q_stag:.2f} MW/m^2)")

        # 3. Real-gas shock layer temperature verification
        t0, real_gas = self.evaluate_real_gas_shock_temperature(telem.ambient_temp_k, telem.mach_number)
        if t0 > self.max_uhtc_temp_k:
            anomalies.append(f"Post-shock stagnation temperature {t0:.0f}K exceeds 2500K UHTC threshold")

        # 4. Scramjet isolator shock train stability & unstart hazard
        _, margin, isolator_ok = self.evaluate_scramjet_isolator_stability(
            telem.isolator_length_m, telem.isolator_height_m, telem.combustor_pressure_ratio
        )
        if not isolator_ok:
            anomalies.append(f"CRITICAL: Scramjet isolator margin {margin:.2f} below 1.25; UNSTART IMMINENT")

        if telem.unstart_actuator_latency_ms > 5.0:
            anomalies.append(f"Actuator response latency ({telem.unstart_actuator_latency_ms:.1f}ms) exceeds 5.0ms unstart limit")

        # Emergency trip conditions
        if margin < 1.05 or tps_sf < 1.10:
            self.is_emergency_scram_active = True
            self.abort_reason = "CRITICAL HYPERSONIC EXCURSION: Executing fuel cut-off and cowl shock dump"

        return (len(anomalies) == 0, anomalies)

    def trigger_unstart_mitigation(self) -> Dict[str, str]:
        """Rapid fuel modulation and cowl boundary-layer bleed to arrest shock migration."""
        self.is_emergency_scram_active = True
        return {
            "status": "UNSTART_MITIGATION_DEPLOYED",
            "fuel_throttle": "REDUCED_TO_CHOKE_MARGIN",
            "bleed_doors": "OPENED_100_PERCENT",
            "actuation_latency_ms": "2.8"
        }
'''
