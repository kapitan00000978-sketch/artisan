"""Empirical references and physical constants for Subsea Autonomous Robotics & Deep-Sea Navigation.

Maintained by Commander Orion 'The Deep' Sterling.
Enforces Full Ocean Depth (11,000m) hydrostatic crush envelopes,
Mackenzie sound speed acoustics, dielectric pressure compensation, and passive ballast fail-safes.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# Gravitational acceleration on Earth (m/s^2)
STANDARD_GRAVITY: float = 9.80665

# Standard seawater density at full ocean depth (kg/m^3)
SEAWATER_DENSITY_SURFACE: float = 1025.0
SEAWATER_DENSITY_HADAL: float = 1035.0
AVERAGE_HADAL_DENSITY: float = 1030.0


@dataclass(frozen=True)
class HydrostaticHullSpec:
    """Specification and safety parameters for subsea pressure hull."""
    material: str
    depth_rating_m: float
    collapse_pressure_mpa: float
    operating_pressure_mpa: float
    safety_factor: float
    inner_diameter_m: float
    wall_thickness_mm: float
    yield_strength_mpa: float

    def is_hadal_certified(self) -> bool:
        """Verify if hull meets Full Ocean Depth (11,000m) standards with >= 1.50 safety margin."""
        return (
            self.depth_rating_m >= 11000.0 and
            self.operating_pressure_mpa >= 110.0 and
            self.safety_factor >= 1.50
        )


@dataclass(frozen=True)
class AcousticNavState:
    """Subsea acoustic localization state and sound speed calibration."""
    sound_speed_mps: float
    dvl_bottom_lock: bool
    usbl_fix_valid: bool
    position_uncertainty_m: float
    max_drift_threshold_m: float = 2.0
    acoustic_multipath_detected: bool = False

    def is_navigation_reliable(self) -> bool:
        """Verify acoustic navigation bounds."""
        return (
            1450.0 <= self.sound_speed_mps <= 1550.0 and
            self.dvl_bottom_lock and
            self.position_uncertainty_m <= self.max_drift_threshold_m and
            not self.acoustic_multipath_detected
        )


@dataclass(frozen=True)
class BuoyancySystemState:
    """Variable buoyancy engine and emergency ballast jettison parameters."""
    displacement_volume_m3: float
    vehicle_dry_mass_kg: float
    net_buoyancy_n: float
    passive_drop_weight_kg: float
    emergency_jettison_time_s: float
    fail_safe_burn_wire_armed: bool

    def is_buoyancy_safe(self) -> bool:
        """Ensure near-neutral trim and sub-30s passive ballast drop."""
        return (
            abs(self.net_buoyancy_n) <= 5.0 and
            self.passive_drop_weight_kg >= 25.0 and
            self.emergency_jettison_time_s <= 30.0 and
            self.fail_safe_burn_wire_armed
        )


@dataclass(frozen=True)
class PressureCompensationState:
    """Dielectric fluid pressure compensation and electrical isolation state."""
    reservoir_bias_pressure_bar: float
    dielectric_fluid_type: str
    insulation_resistance_mohm: float
    seawater_leak_detected: bool = False
    ambient_pressure_bar: float = 1100.0

    def is_compensation_intact(self) -> bool:
        """Verify positive internal gauge pressure and electrical isolation."""
        return (
            self.reservoir_bias_pressure_bar >= 0.20 and
            self.insulation_resistance_mohm >= 10.0 and
            not self.seawater_leak_detected
        )


@dataclass
class SubseaMissionReport:
    """Comprehensive subsea autonomy and extreme depth safety evaluation."""
    mission_id: str
    hull_integrity_verified: bool
    navigation_valid: bool
    buoyancy_stable: bool
    compensation_secure: bool
    safety_score: float
    anomalies: List[str] = field(default_factory=list)
    summary: str = ""


def calculate_hydrostatic_pressure(depth_m: float, density_kg_m3: float = AVERAGE_HADAL_DENSITY) -> float:
    """Calculate hydrostatic pressure in MPa at depth in meters.
    P = rho * g * h * 1e-6 (MPa)
    """
    if depth_m < 0.0:
        raise ValueError("Depth cannot be negative.")
    return (density_kg_m3 * STANDARD_GRAVITY * depth_m) * 1e-6


def calculate_sound_speed_mackenzie(temperature_c: float, salinity_ppt: float, depth_m: float) -> float:
    """Calculate speed of sound in seawater using the 9-term Mackenzie (1981) empirical formula.
    
    Valid for:
    Temperature: 2 to 30 deg C
    Salinity: 25 to 40 ppt
    Depth: 0 to 8000 m (extrapolates smoothly to hadal depths)
    """
    t = temperature_c
    s = salinity_ppt
    d = depth_m

    t2 = t * t
    t3 = t2 * t
    d2 = d * d
    d3 = d2 * d

    c = (
        1448.96
        + 4.591 * t
        - 5.304e-2 * t2
        + 2.374e-4 * t3
        + 1.340 * (s - 35.0)
        + 1.630e-2 * d
        + 1.675e-7 * d2
        - 1.025e-2 * t * (s - 35.0)
        - 7.139e-13 * t * d3
    )
    return c


def evaluate_hull_safety_factor(collapse_pressure_mpa: float, operating_pressure_mpa: float) -> float:
    """Evaluate structural collapse safety factor."""
    if operating_pressure_mpa <= 0.0:
        raise ValueError("Operating pressure must be positive.")
    return collapse_pressure_mpa / operating_pressure_mpa


def evaluate_net_buoyancy(
    displacement_m3: float,
    vehicle_mass_kg: float,
    water_density_kg_m3: float = AVERAGE_HADAL_DENSITY
) -> float:
    """Evaluate net buoyancy in Newtons.
    Positive: buoyant (floats up). Negative: heavy (sinks).
    """
    buoyant_force_n = displacement_m3 * water_density_kg_m3 * STANDARD_GRAVITY
    gravity_force_n = vehicle_mass_kg * STANDARD_GRAVITY
    return buoyant_force_n - gravity_force_n


class DeepSeaReferenceLibrary:
    """Empirical bounds and canonical reference implementation for Deep-Sea Autonomous Robotics."""

    # Absolute Hadal Depth and Structural Thresholds
    HADAL_CHALLENGER_DEPTH_M: float = 11000.0
    MIN_COLLAPSE_SAFETY_FACTOR: float = 1.50
    MIN_HYDROSTATIC_PRESSURE_RATING_MPA: float = 110.0

    # Acoustic Navigation Bounds
    SOUND_SPEED_MIN_MPS: float = 1450.0
    SOUND_SPEED_MAX_MPS: float = 1550.0
    MAX_NAV_DRIFT_UNCERTAINTY_M: float = 2.00

    # Pressure Compensation & Electrical Thresholds
    MIN_COMPENSATION_BIAS_BAR: float = 0.20
    MIN_INSULATION_RESISTANCE_MOHM: float = 10.0
    CRITICAL_INSULATION_ABORT_MOHM: float = 1.0

    # Buoyancy and Emergency Ballast Thresholds
    MAX_NEUTRAL_BUOYANCY_OFFSET_N: float = 5.0
    MAX_PASSIVE_JETTISON_TIME_S: float = 30.0
    MIN_DROP_WEIGHT_KG: float = 25.0

    @classmethod
    def get_canonical_core(cls) -> str:
        """Returns reference production-grade implementation for deep-sea AUV core autonomy."""
        return r'''"""Canonical Autonomous Deep-Sea Vehicle (AUV) Hadal Autonomy Core.
Authored to the strict physical benchmarks of Commander Orion Sterling.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class DeepSeaTelemetry:
    depth_m: float
    ambient_pressure_mpa: float
    sound_speed_mps: float
    dvl_locked: bool
    position_error_m: float
    compensation_bias_bar: float
    insulation_mohm: float
    net_buoyancy_n: float
    drop_weight_armed: bool


class HadalAutonomyExecutive:
    """Deterministic executive managing Full Ocean Depth safety envelopes."""

    def __init__(self, max_depth_m: float = 11000.0) -> None:
        self.max_depth_m = max_depth_m
        self.min_safety_factor = 1.50
        self.rated_hull_collapse_mpa = 175.0  # Grade 5 Titanium sphere collapse rating
        self.is_emergency_abort_active = False
        self.abort_reason: Optional[str] = None

    def compute_hydrostatic_pressure(self, depth_m: float) -> float:
        """Calculate hydrostatic pressure in MPa (density = 1030 kg/m^3)."""
        density = 1030.0
        gravity = 9.80665
        return (density * gravity * depth_m) * 1e-6

    def calculate_sound_velocity(self, temp_c: float, salinity_ppt: float, depth_m: float) -> float:
        """Evaluate Mackenzie sound velocity profile."""
        t, s, d = temp_c, salinity_ppt, depth_m
        t2, t3, d2, d3 = t * t, t * t * t, d * d, d * d * d
        return (
            1448.96
            + 4.591 * t
            - 5.304e-2 * t2
            + 2.374e-4 * t3
            + 1.340 * (s - 35.0)
            + 1.630e-2 * d
            + 1.675e-7 * d2
            - 1.025e-2 * t * (s - 35.0)
            - 7.139e-13 * t * d3
        )

    def verify_hull_safety(self, depth_m: float) -> Tuple[bool, float]:
        """Verify hydrostatic pressure vs collapse rating safety factor."""
        p_operating = self.compute_hydrostatic_pressure(depth_m)
        safety_factor = self.rated_hull_collapse_mpa / max(p_operating, 1e-3)
        return (safety_factor >= self.min_safety_factor, safety_factor)

    def evaluate_telemetry_safety(self, telem: DeepSeaTelemetry) -> Tuple[bool, List[str]]:
        """Ruthlessly verify subsea telemetry against physical hadal invariants."""
        anomalies: List[str] = []

        # 1. Structural crush check
        p_calc = self.compute_hydrostatic_pressure(telem.depth_m)
        sf = self.rated_hull_collapse_mpa / max(p_calc, 1e-3)
        if sf < 1.50:
            anomalies.append(f"CRITICAL: Hull safety factor below 1.50 (SF={sf:.2f})")

        # 2. Acoustic navigation fidelity
        if not (1450.0 <= telem.sound_speed_mps <= 1550.0):
            anomalies.append(f"Acoustic sound speed out of bounds: {telem.sound_speed_mps:.1f} m/s")
        if not telem.dvl_locked:
            anomalies.append("DVL bottom-lock lost; dead reckoning degraded")
        if telem.position_error_m > 2.0:
            anomalies.append(f"Position drift error {telem.position_error_m:.2f}m exceeds 2.0m bound")

        # 3. Dielectric pressure compensation
        if telem.compensation_bias_bar < 0.20:
            anomalies.append(f"Compensator bias {telem.compensation_bias_bar:.2f} bar below 0.20 bar")
        if telem.insulation_mohm < 10.0:
            anomalies.append(f"Insulation resistance degraded to {telem.insulation_mohm:.1f} MOhm")

        # 4. Buoyancy & Fail-safe drop weights
        if abs(telem.net_buoyancy_n) > 5.0:
            anomalies.append(f"Neutral buoyancy offset {telem.net_buoyancy_n:.1f}N exceeds 5.0N trim")
        if not telem.drop_weight_armed:
            anomalies.append("Emergency passive drop weight fail-safe NOT armed")

        # Emergency abort condition
        if telem.insulation_mohm < 1.0 or sf < 1.30 or telem.compensation_bias_bar < 0.05:
            self.is_emergency_abort_active = True
            self.abort_reason = "CRITICAL SUBSEA FAULT: Executing passive drop-weight ascent"

        return (len(anomalies) == 0, anomalies)

    def trigger_passive_jettison(self) -> Dict[str, str]:
        """Trigger burn-wire galvanic ballast drop for autonomous passive ascent."""
        self.is_emergency_abort_active = True
        return {
            "status": "BALLAST_DROPPED",
            "jettison_method": "GALVANIC_BURN_WIRE",
            "expected_ascent_speed_mps": "1.2",
            "buoyancy_gain_newtons": "+250.0"
        }
'''
