"""Nuclear Reactor Physics, Neutron Kinetics & Criticality Safety Standards.

Author: Dr. Magnus 'The Core' Sterling
Status: Production Reference Standard
"""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Physical & Engineering Constants
BETA_EFF_U235: float = 0.0065  # Effective delayed neutron fraction
PROMPT_NEUTRON_LIFETIME_SEC: float = 1.0e-4  # Lambda (seconds)
MAX_TRANSIENT_REACTIVITY_DOLLARS: float = 0.80  # Safe limit below prompt critical ($1.00)
MAX_SHUTDOWN_KEFF: float = 0.950  # Cold subcritical shutdown limit
MIN_DNBR_THRESHOLD: float = 1.30  # Departure from Nucleate Boiling Ratio limit
MAX_SCRAM_INSERTION_TIME_SEC: float = 2.5  # Seconds for full gravity SCRAM
MAX_DOPPLER_COEFF_PCM_K: float = -1.5  # Must be strictly negative (pcm / Kelvin)

# Standard Keepin 6-Group Delayed Neutron Parameters for U-235 Thermal Fission
DEFAULT_6_GROUP_PRECURSORS = (
    (0.000215, 0.0124),  # Group 1
    (0.001424, 0.0305),  # Group 2
    (0.001274, 0.1110),  # Group 3
    (0.002568, 0.3010),  # Group 4
    (0.000748, 1.1400),  # Group 5
    (0.000273, 3.0100),  # Group 6
)


@dataclass(frozen=True)
class DelayedPrecursorGroup:
    """Represents one of the 6 standard delayed neutron precursor groups."""
    group_id: int
    fraction_beta: float
    decay_constant_lambda: float


@dataclass
class ReactivityState:
    """Core reactivity and temperature feedback state."""
    keff: float
    fuel_temp_k: float = 900.0
    mod_temp_k: float = 580.0
    doppler_coeff_pcm_k: float = MAX_DOPPLER_COEFF_PCM_K
    mtc_pcm_k: float = -10.0

    def reactivity(self) -> float:
        """Compute dimensionless reactivity rho = (keff - 1) / keff."""
        if self.keff <= 0.0:
            return -1.0
        return (self.keff - 1.0) / self.keff

    def reactivity_pcm(self) -> float:
        """Compute reactivity in percent-milli (pcm = rho * 10^5)."""
        return self.reactivity() * 100000.0

    def reactivity_dollars(self, beta_eff: float = BETA_EFF_U235) -> float:
        """Compute reactivity in dollars ($ = rho / beta_eff). Prompt critical is $1.00."""
        return self.reactivity() / beta_eff

    def is_prompt_critical(self, beta_eff: float = BETA_EFF_U235) -> bool:
        """Check if reactivity meets or exceeds prompt critical ($ >= 1.00)."""
        return self.reactivity_dollars(beta_eff=beta_eff) >= 1.00

    def is_passively_safe(self) -> Tuple[bool, List[str]]:
        """Verify core obeys passive feedback invariants (negative Doppler coefficient)."""
        reasons = []
        if self.doppler_coeff_pcm_k >= 0.0:
            reasons.append(
                f"Catastrophic positive Doppler coefficient: alpha_f = {self.doppler_coeff_pcm_k:.2f} pcm/K >= 0"
            )
        if self.is_prompt_critical():
            reasons.append(
                f"Prompt critical hazard: reactivity {self.reactivity_dollars():.2f}$ >= 1.00$ threshold"
            )
        elif self.reactivity_dollars() > MAX_TRANSIENT_REACTIVITY_DOLLARS:
            reasons.append(
                f"Reactivity exceeds safe transient limit: {self.reactivity_dollars():.2f}$ > {MAX_TRANSIENT_REACTIVITY_DOLLARS}$"
            )
        return len(reasons) == 0, reasons


class PointReactorKineticsSolver:
    """Deterministic Point Reactor Kinetics Equations (PRKE) with 6-group delayed precursors."""

    def __init__(
        self,
        beta_eff: float = BETA_EFF_U235,
        prompt_lifetime_sec: float = PROMPT_NEUTRON_LIFETIME_SEC,
        precursor_params: Tuple[Tuple[float, float], ...] = DEFAULT_6_GROUP_PRECURSORS,
    ):
        self.beta_eff = beta_eff
        self.prompt_lifetime = prompt_lifetime_sec
        self.precursor_groups = [
            DelayedPrecursorGroup(i + 1, beta, lam) for i, (beta, lam) in enumerate(precursor_params)
        ]

    def equilibrium_precursors(self, steady_neutron_density: float) -> List[float]:
        """Compute initial equilibrium precursor concentrations for steady state dn/dt = 0."""
        precursors = []
        for g in self.precursor_groups:
            # At steady state: dC_i/dt = 0 => C_i = (beta_i / (lambda_i * Lambda)) * n0
            c_i = (g.fraction_beta / (g.decay_constant_lambda * self.prompt_lifetime)) * steady_neutron_density
            precursors.append(c_i)
        return precursors

    def step(
        self,
        dt_sec: float,
        neutron_density: float,
        precursors: List[float],
        reactivity: float,
    ) -> Tuple[float, List[float]]:
        """Advance PRKE system by dt using deterministic numerical integration."""
        if len(precursors) != len(self.precursor_groups):
            raise ValueError(f"Expected {len(self.precursor_groups)} precursor groups, got {len(precursors)}")

        # dn/dt = ((rho - beta) / Lambda) * n + sum(lambda_i * C_i)
        prompt_term = ((reactivity - self.beta_eff) / self.prompt_lifetime) * neutron_density
        delayed_term = sum(g.decay_constant_lambda * c for g, c in zip(self.precursor_groups, precursors))
        dn_dt = prompt_term + delayed_term

        # dC_i/dt = (beta_i / Lambda) * n - lambda_i * C_i
        new_precursors = []
        for g, c in zip(self.precursor_groups, precursors):
            dc_dt = (g.fraction_beta / self.prompt_lifetime) * neutron_density - (g.decay_constant_lambda * c)
            new_c = max(0.0, c + dc_dt * dt_sec)
            new_precursors.append(new_c)

        new_n = max(0.0, neutron_density + dn_dt * dt_sec)
        return new_n, new_precursors


@dataclass
class ThermalHydraulicsSafety:
    """Core thermal margin and Departure from Nucleate Boiling Ratio (DNBR) validator."""
    local_heat_flux_kw_m2: float
    critical_heat_flux_kw_m2: float

    def dnbr(self) -> float:
        """Compute Departure from Nucleate Boiling Ratio DNBR = CHF / local_heat_flux."""
        if self.local_heat_flux_kw_m2 <= 0.0:
            return float("inf")
        return self.critical_heat_flux_kw_m2 / self.local_heat_flux_kw_m2

    def is_thermal_margin_acceptable(self, min_threshold: float = MIN_DNBR_THRESHOLD) -> bool:
        """Verify DNBR remains strictly above the regulatory thermal safety limit."""
        return self.dnbr() >= min_threshold


@dataclass
class ControlRodBank:
    """Emergency SCRAM control rod cluster bank with N-1 stuck rod redundancy modeling."""
    bank_name: str
    worth_pcm: float
    insertion_time_sec: float
    is_stuck: bool = False

    def can_scram_within_limit(self, max_time_sec: float = MAX_SCRAM_INSERTION_TIME_SEC) -> bool:
        """Verify rod insertion meets gravity drop time limit."""
        return not self.is_stuck and self.insertion_time_sec <= max_time_sec


class NuclearReferenceLibrary:
    """Canonical repository of nuclear reactor physics & criticality safety benchmarks."""

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        return {
            "beta_eff_u235": BETA_EFF_U235,
            "prompt_lifetime_sec": PROMPT_NEUTRON_LIFETIME_SEC,
            "max_transient_dollars": MAX_TRANSIENT_REACTIVITY_DOLLARS,
            "max_shutdown_keff": MAX_SHUTDOWN_KEFF,
            "min_dnbr": MIN_DNBR_THRESHOLD,
            "max_scram_time_sec": MAX_SCRAM_INSERTION_TIME_SEC,
            "max_doppler_coeff_pcm_k": MAX_DOPPLER_COEFF_PCM_K,
        }

    @staticmethod
    def get_anti_patterns() -> List[str]:
        return [
            "Operating with or projecting positive fuel Doppler temperature coefficient (alpha_f >= 0)",
            "Inserting reactivity exceeding delayed neutron fraction into prompt critical regime ($ >= 1.00)",
            "Ignoring 6-group delayed neutron precursor kinetics during transient calculations",
            "Permitting local Departure from Nucleate Boiling Ratio DNBR < 1.30 causing cladding dryout",
            "Emergency SCRAM insertion time exceeding 2.5 seconds or failing N-1 stuck rod shutdown margin",
            "Maintaining subcritical storage or refueling margin with keff > 0.95",
        ]

    @staticmethod
    def get_criticality_checklist() -> List[str]:
        return [
            "Verify strictly negative Doppler fuel temperature coefficient (alpha_f <= -1.5 pcm/K)",
            "Ensure core reactivity remains bounded below $0.80 under all control rod withdrawals",
            "Couple 6-group delayed neutron precursor differential equations in all kinetics calculations",
            "Monitor local heat flux to maintain minimum DNBR >= 1.30 against critical heat flux",
            "Perform N-1 stuck rod analysis verifying shutdown margin keff <= 0.95 with gravity SCRAM <= 2.5s",
            "Enforce automatic fast SCRAM trip setpoints on over-power (118%) and low DNBR (<1.30)",
        ]

    @staticmethod
    def get_canonical_core() -> str:
        return r'''"""Canonical Nuclear Reactor Physics & Criticality Safety Engine.
Standards: 6-Group PRKE, Negative Doppler Feedback, DNBR >= 1.30, SCRAM <= 2.5s
"""

from typing import Dict, Any, List, Tuple

BETA_EFF = 0.0065
PROMPT_LIFETIME = 1.0e-4
MIN_DNBR = 1.30
MAX_SCRAM_TIME = 2.5

class ReactivityState:
    """Core reactivity and Doppler temperature feedback."""

    def __init__(self, keff: float, doppler_pcm_k: float = -2.5):
        self.keff = keff
        self.doppler_pcm_k = doppler_pcm_k

    def reactivity(self) -> float:
        return (self.keff - 1.0) / self.keff if self.keff > 0 else -1.0

    def reactivity_dollars(self) -> float:
        return self.reactivity() / BETA_EFF

    def is_safe(self) -> bool:
        return self.doppler_pcm_k < 0.0 and self.reactivity_dollars() <= 0.80

class PointReactorKineticsSolver:
    """6-Group Delayed Neutron Point Reactor Kinetics Solver."""

    def __init__(self):
        self.precursor_betas = [0.000215, 0.001424, 0.001274, 0.002568, 0.000748, 0.000273]
        self.precursor_lambdas = [0.0124, 0.0305, 0.1110, 0.3010, 1.1400, 3.0100]

    def step(self, dt: float, n: float, precursors: List[float], rho: float) -> Tuple[float, List[float]]:
        prompt = ((rho - BETA_EFF) / PROMPT_LIFETIME) * n
        delayed = sum(lam * c for lam, c in zip(self.precursor_lambdas, precursors))
        dn_dt = prompt + delayed
        new_precursors = []
        for beta, lam, c in zip(self.precursor_betas, self.precursor_lambdas, precursors):
            dc_dt = (beta / PROMPT_LIFETIME) * n - lam * c
            new_precursors.append(max(0.0, c + dc_dt * dt))
        new_n = max(0.0, n + dn_dt * dt)
        return new_n, new_precursors

def verify_thermal_dnbr(local_heat_flux: float, critical_heat_flux: float) -> bool:
    dnbr = critical_heat_flux / local_heat_flux if local_heat_flux > 0 else float("inf")
    return dnbr >= MIN_DNBR

def verify_scram_shutdown(insertion_time: float, is_stuck: bool = False) -> bool:
    return not is_stuck and insertion_time <= MAX_SCRAM_TIME
'''
