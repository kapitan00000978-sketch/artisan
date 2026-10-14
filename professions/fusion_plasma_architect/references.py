"""Tokamak Magnetic Confinement, MHD Stability & Fusion Plasma Standards.

Author: Dr. Silas 'The Plasma' Vance
Status: Production Reference Standard
"""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Physical & Engineering Constants
MIN_SAFETY_FACTOR_Q95: float = 3.0  # Safe edge safety factor (Kruskal-Shafranov is > 2.0)
KRUSKAL_SHAFRANOV_MIN_Q: float = 2.0  # Absolute hard boundary against external kink disruptions
MAX_TROYON_BETA_N: float = 3.5  # Maximum normalized beta limit (% * m * T / MA)
MAX_GREENWALD_FRACTION: float = 0.85  # Line-averaged density fraction limit (f_G = n / n_G)
MAX_DIVERTOR_HEAT_FLUX_MW_M2: float = 10.0  # Technological cooling limit of tungsten monoblocks
MAX_ISLAND_WIDTH_RATIO: float = 0.05  # Maximum tolerable magnetic island size w / a
MIN_RADIATIVE_FRACTION: float = 0.70  # Divertor detachment radiative power fraction


@dataclass
class PlasmaEquilibrium:
    """Core macroscopic parameters of a toroidal tokamak plasma equilibrium."""
    major_radius_r0_m: float
    minor_radius_a_m: float
    b_toroidal_t: float
    plasma_current_ma: float
    electron_density_1e20: float
    central_temperature_kev: float

    def aspect_ratio(self) -> float:
        """Compute torus aspect ratio A = R_0 / a."""
        if self.minor_radius_a_m <= 0:
            return float("inf")
        return self.major_radius_r0_m / self.minor_radius_a_m

    def cylindrical_safety_factor(self) -> float:
        """Compute cylindrical estimate of safety factor q_cyl."""
        if self.plasma_current_ma <= 0:
            return float("inf")
        # q_cyl ~ (5 * a^2 * B_T) / (R_0 * I_p)
        return (5.0 * (self.minor_radius_a_m ** 2) * self.b_toroidal_t) / (
            self.major_radius_r0_m * self.plasma_current_ma
        )


@dataclass
class SafetyFactorProfile:
    """Radial safety factor q profile monitoring Kruskal-Shafranov limits."""
    q0: float = 1.05
    q95: float = 3.20

    def is_kruskal_shafranov_stable(self) -> Tuple[bool, List[str]]:
        """Verify safety factor profile against external kink and sawtooth boundaries."""
        reasons = []
        if self.q95 < KRUSKAL_SHAFRANOV_MIN_Q:
            reasons.append(
                f"Catastrophic external kink disruption: q95 = {self.q95:.2f} < {KRUSKAL_SHAFRANOV_MIN_Q:.2f}"
            )
        elif self.q95 < MIN_SAFETY_FACTOR_Q95:
            reasons.append(
                f"Sub-optimal edge safety factor: q95 = {self.q95:.2f} < {MIN_SAFETY_FACTOR_Q95:.2f} safe margin"
            )
        if self.q0 < 0.90:
            reasons.append(f"Severe core sawtooth crash hazard: q0 = {self.q0:.2f} < 0.90")
        return len(reasons) == 0, reasons


@dataclass
class TroyonBetaMonitor:
    """Evaluates normalized plasma beta against the Troyon MHD stability limit."""
    beta_total_pct: float
    minor_radius_m: float
    b_toroidal_t: float
    plasma_current_ma: float

    def normalized_beta(self) -> float:
        """Compute normalized beta beta_N = beta(%) * (a * B_T) / I_p."""
        if self.plasma_current_ma <= 0:
            return float("inf")
        return self.beta_total_pct * (self.minor_radius_m * self.b_toroidal_t) / self.plasma_current_ma

    def is_within_troyon_limit(self, limit: float = MAX_TROYON_BETA_N) -> bool:
        """Check if plasma operates below Troyon ideal MHD limit."""
        return self.normalized_beta() <= limit


@dataclass
class GreenwaldDensityMonitor:
    """Evaluates line-averaged electron density against the Greenwald empirical limit."""
    electron_density_1e20: float
    plasma_current_ma: float
    minor_radius_m: float

    def greenwald_limit_1e20(self) -> float:
        """Compute Greenwald density limit n_G = I_p / (pi * a^2) in 10^20 m^-3."""
        if self.minor_radius_m <= 0:
            return 0.0
        cross_section_area = math.pi * (self.minor_radius_m ** 2)
        return self.plasma_current_ma / cross_section_area

    def greenwald_fraction(self) -> float:
        """Compute Greenwald density fraction f_G = n_e / n_G."""
        ng = self.greenwald_limit_1e20()
        if ng <= 0:
            return float("inf")
        return self.electron_density_1e20 / ng

    def is_safe_from_density_limit_disruption(self, max_fraction: float = MAX_GREENWALD_FRACTION) -> bool:
        """Verify operating density has safe margin below radiative collapse."""
        return self.greenwald_fraction() <= max_fraction


@dataclass
class NeoclassicalTearingMode:
    """Evaluates magnetic island width at rational surfaces and ECCD microwave stabilization."""
    rational_surface_q: float
    island_width_m: float
    minor_radius_m: float
    eccd_power_mw: float = 0.0

    def island_width_ratio(self) -> float:
        """Compute relative island size w / a."""
        if self.minor_radius_m <= 0:
            return float("inf")
        return self.island_width_m / self.minor_radius_m

    def is_stabilized(self, max_ratio: float = MAX_ISLAND_WIDTH_RATIO) -> bool:
        """Verify island remains small or is actively suppressed by ECCD."""
        ratio = self.island_width_ratio()
        if ratio <= max_ratio:
            return True
        # If island is large, ECCD power must be actively applied to shrink it
        return self.eccd_power_mw >= 5.0


@dataclass
class DivertorThermalProtection:
    """Monitors peak divertor heat exhaust against tungsten tile burnout limits."""
    peak_heat_flux_mw_m2: float
    radiative_fraction: float

    def is_divertor_protected(
        self,
        max_heat_flux: float = MAX_DIVERTOR_HEAT_FLUX_MW_M2,
        min_rad_fraction: float = MIN_RADIATIVE_FRACTION,
    ) -> bool:
        """Verify divertor operates in detached/semi-detached regime within cooling limits."""
        return (
            self.peak_heat_flux_mw_m2 <= max_heat_flux and
            self.radiative_fraction >= min_rad_fraction
        )


class FusionReferenceLibrary:
    """Canonical repository of tokamak plasma physics and disruption mitigation standards."""

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        return {
            "min_q95": MIN_SAFETY_FACTOR_Q95,
            "kruskal_shafranov_q": KRUSKAL_SHAFRANOV_MIN_Q,
            "max_troyon_beta_n": MAX_TROYON_BETA_N,
            "max_greenwald_fraction": MAX_GREENWALD_FRACTION,
            "max_divertor_heat_flux_mw_m2": MAX_DIVERTOR_HEAT_FLUX_MW_M2,
            "max_island_width_ratio": MAX_ISLAND_WIDTH_RATIO,
            "min_radiative_fraction": MIN_RADIATIVE_FRACTION,
        }

    @staticmethod
    def get_anti_patterns() -> List[str]:
        return [
            "Operating with edge safety factor q95 < 2.0 provoking catastrophic external kink disruption",
            "Exceeding Greenwald density ceiling f_G > 1.0 causing edge radiative collapse and MARFE",
            "Operating above Troyon normalized beta limit beta_N > 3.5 without active wall stabilization",
            "Allowing magnetic islands (w > 0.05 a) to grow and lock to the vacuum vessel without ECCD",
            "Directing unmitigated divertor heat exhaust exceeding 10 MW/m^2 onto tungsten monoblocks",
            "Relying on human intervention instead of sub-10ms automated disruption mitigation (SPI/MGI)",
        ]

    @staticmethod
    def get_disruption_avoidance_checklist() -> List[str]:
        return [
            "Maintain edge safety factor q95 >= 3.0 via active plasma current ramp and shaping control",
            "Enforce gas puffing control keeping Greenwald density fraction f_G <= 0.85",
            "Monitor normalized beta beta_N <= 3.5 and regulate auxiliary NBI/ICRH heating",
            "Detect rational surface islands and steer real-time localized ECCD for NTM suppression",
            "Seed nitrogen/argon impurities to achieve radiative detachment with f_rad >= 0.70",
            "Arm fast Shattered Pellet Injection (SPI) triggering on precursor lock within 10 ms",
        ]

    @staticmethod
    def get_canonical_core() -> str:
        return r'''"""Canonical Tokamak Magnetic Confinement & Plasma Stability Engine.
Standards: q95 >= 3.0, Troyon Beta_N <= 3.5, Greenwald f_G <= 0.85, Divertor <= 10 MW/m^2
"""

import math
from typing import Dict, Any, List, Tuple

MIN_Q95 = 3.0
MAX_BETA_N = 3.5
MAX_GREENWALD_FRAC = 0.85
MAX_DIVERTOR_FLUX = 10.0

class SafetyFactorProfile:
    """Monitors safety factor profile against Kruskal-Shafranov kink disruption."""

    def __init__(self, q0: float = 1.05, q95: float = 3.20):
        self.q0 = q0
        self.q95 = q95

    def is_kink_stable(self) -> bool:
        return self.q95 >= MIN_Q95 and self.q0 >= 0.95

class TroyonBetaMonitor:
    """Evaluates normalized beta against Troyon ideal MHD limit."""

    def __init__(self, beta_pct: float, a_m: float, bt_t: float, ip_ma: float):
        self.beta_pct = beta_pct
        self.a_m = a_m
        self.bt_t = bt_t
        self.ip_ma = ip_ma

    def beta_n(self) -> float:
        if self.ip_ma <= 0:
            return float("inf")
        return self.beta_pct * (self.a_m * self.bt_t) / self.ip_ma

    def is_stable(self) -> bool:
        return self.beta_n() <= MAX_BETA_N

class GreenwaldDensityMonitor:
    """Evaluates line-averaged electron density against Greenwald density limit."""

    def __init__(self, ne_1e20: float, ip_ma: float, a_m: float):
        self.ne_1e20 = ne_1e20
        self.ip_ma = ip_ma
        self.a_m = a_m

    def greenwald_limit(self) -> float:
        return self.ip_ma / (math.pi * (self.a_m ** 2)) if self.a_m > 0 else 0.0

    def greenwald_fraction(self) -> float:
        ng = self.greenwald_limit()
        return self.ne_1e20 / ng if ng > 0 else float("inf")

    def is_safe(self) -> bool:
        return self.greenwald_fraction() <= MAX_GREENWALD_FRAC

def verify_ntm_stabilization(island_width_m: float, a_m: float, eccd_power_mw: float) -> bool:
    ratio = island_width_m / a_m if a_m > 0 else float("inf")
    return ratio <= 0.05 or eccd_power_mw >= 5.0

def verify_divertor_safety(peak_flux_mw_m2: float, radiative_fraction: float) -> bool:
    return peak_flux_mw_m2 <= MAX_DIVERTOR_FLUX and radiative_fraction >= 0.70
'''
