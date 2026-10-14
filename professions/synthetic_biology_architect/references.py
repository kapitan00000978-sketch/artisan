"""Empirical references and biochemical constants for Synthetic Biology & Metabolic Genetic Circuits.

Maintained by Dr. Seraphiel 'The SynBio' Sterling.
Enforces non-linear Hill cooperativity, cellular metabolic burden thresholds,
orthogonal transcriptional isolation, and multi-layer biocontainment escape bounds.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class HillKineticsState:
    """Biochemical transcription transfer function governed by Hill kinetics."""
    max_expression_au: float
    kd_umolar: float
    hill_coefficient_n: float
    basal_expression_au: float
    dynamic_range_ratio: float

    def is_kinetics_robust(self) -> bool:
        """Verify Hill cooperativity n >= 2.0 and dynamic range ON/OFF >= 20.0."""
        return (
            self.hill_coefficient_n >= 2.0 and
            self.dynamic_range_ratio >= 20.0 and
            self.basal_expression_au < (self.max_expression_au / 20.0)
        )


@dataclass(frozen=True)
class MetabolicBurdenState:
    """Host chassis metabolic drain and resource allocation."""
    ribosome_allocation_fraction: float
    atp_drain_fraction: float
    total_burden_fraction: float
    host_growth_rate_ratio: float

    def is_burden_sustainable(self) -> bool:
        """Ensure synthetic circuit consumes <= 30% host translation/energy budget."""
        return (
            self.total_burden_fraction <= 0.30 and
            self.host_growth_rate_ratio >= 0.70
        )


@dataclass(frozen=True)
class OrthogonalRegulonState:
    """Transcriptional and translational orthogonality."""
    promoter_identity: str
    transcription_factor: str
    host_crosstalk_fraction: float
    translation_fidelity_pct: float

    def is_orthogonal_clean(self) -> bool:
        """Verify host crosstalk <= 5% and translation fidelity >= 98%."""
        return (
            self.host_crosstalk_fraction <= 0.05 and
            self.translation_fidelity_pct >= 98.0
        )


@dataclass(frozen=True)
class BiocontainmentState:
    """Biosafety containment mechanisms and suicide kill switches."""
    synthetic_auxotrophy_nutrient: str
    suicide_switch_mechanism: str
    measured_escape_frequency: float
    kill_switch_latency_min: float
    is_dual_layer_contained: bool

    def is_containment_secure(self) -> bool:
        """Verify escape frequency <= 1e-8 (NIH recombinant DNA standard) and dual-layer."""
        return (
            self.measured_escape_frequency <= 1.0e-8 and
            self.kill_switch_latency_min <= 60.0 and
            self.is_dual_layer_contained
        )


@dataclass
class SyntheticBiologyMissionReport:
    """Comprehensive synthetic biology circuit and biocontainment safety audit."""
    strain_id: str
    kinetics_valid: bool
    burden_safe: bool
    orthogonality_ok: bool
    biocontainment_intact: bool
    safety_score: float
    anomalies: List[str] = field(default_factory=list)
    summary: str = ""


def calculate_hill_repression(
    inducer_umolar: float,
    vmax: float = 1000.0,
    kd: float = 10.0,
    n: float = 2.5,
    basal: float = 5.0
) -> float:
    """Calculate transcription rate for a repressive Hill transfer function.
    f(I) = basal + Vmax * (Kd^n) / (Kd^n + I^n)
    """
    if inducer_umolar < 0.0 or kd <= 0.0 or n <= 0.0:
        raise ValueError("Inducer, Kd, and Hill coefficient must be non-negative and positive.")
    kd_n = kd ** n
    i_n = inducer_umolar ** n
    return basal + vmax * (kd_n / (kd_n + i_n))


def calculate_dynamic_range(on_expression_au: float, off_expression_au: float) -> float:
    """Calculate circuit ON/OFF dynamic range ratio."""
    if off_expression_au <= 0.0:
        return float("inf")
    return on_expression_au / off_expression_au


def evaluate_metabolic_burden(
    ribosome_fraction: float,
    atp_fraction: float
) -> float:
    """Evaluate composite cellular metabolic burden fraction."""
    if ribosome_fraction < 0.0 or atp_fraction < 0.0:
        raise ValueError("Resource fractions must be non-negative.")
    return 0.6 * ribosome_fraction + 0.4 * atp_fraction


class SynBioReferenceLibrary:
    """Empirical bounds and canonical reference implementation for Synthetic Biology."""

    MIN_HILL_COOPERATIVITY: float = 2.00
    MIN_DYNAMIC_RANGE: float = 20.0
    MAX_METABOLIC_BURDEN: float = 0.30
    MAX_CROSSTALK_FRACTION: float = 0.05
    MAX_ESCAPE_FREQUENCY: float = 1.0e-8
    MAX_KILL_SWITCH_LATENCY_MIN: float = 60.0

    @classmethod
    def get_canonical_core(cls) -> str:
        """Returns reference production-grade implementation for synthetic biology executive."""
        return r'''"""Canonical Synthetic Biology Genetic Circuit & Biocontainment Executive.
Authored to the strict biochemical benchmarks of Dr. Seraphiel Sterling.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class GeneticCircuitTelemetry:
    strain_id: str
    hill_coefficient: float
    on_expression_au: float
    off_expression_au: float
    ribosome_usage_fraction: float
    atp_drain_fraction: float
    host_crosstalk_rate: float
    escape_frequency: float
    kill_switch_latency_min: float
    auxotrophy_intact: bool


class SynBioAutonomyExecutive:
    """Deterministic executive managing synthetic genetic circuits and biocontainment."""

    def __init__(self) -> None:
        self.min_hill_n = 2.0
        self.min_dynamic_range = 20.0
        self.max_burden_limit = 0.30
        self.max_crosstalk_limit = 0.05
        self.max_escape_freq = 1.0e-8
        self.max_kill_latency_min = 60.0
        self.is_kill_switch_active = False
        self.kill_reason: Optional[str] = None

    def compute_transfer_function(
        self,
        inducer_um: float,
        vmax: float = 1200.0,
        kd: float = 8.5,
        n: float = 2.6,
        basal: float = 12.0
    ) -> float:
        """Evaluate Hill repressive kinetics."""
        kd_n = kd ** n
        i_n = inducer_um ** n
        return basal + vmax * (kd_n / (kd_n + i_n))

    def evaluate_circuit_burden(self, ribo_frac: float, atp_frac: float) -> float:
        """Calculate composite cellular burden index."""
        return 0.6 * ribo_frac + 0.4 * atp_frac

    def evaluate_telemetry_safety(self, telem: GeneticCircuitTelemetry) -> Tuple[bool, List[str]]:
        """Ruthlessly audit synthetic biology telemetry against biophysical and safety standards."""
        anomalies: List[str] = []

        # 1. Hill cooperativity and bistability check
        if telem.hill_coefficient < self.min_hill_n:
            anomalies.append(f"Sub-cooperative Hill coefficient n={telem.hill_coefficient:.2f} < 2.0 (state noise unstable)")

        # 2. Dynamic range ON/OFF ratio
        dyn_range = telem.on_expression_au / max(telem.off_expression_au, 1e-3)
        if dyn_range < self.min_dynamic_range:
            anomalies.append(f"Circuit dynamic range {dyn_range:.1f}x below 20.0x threshold (basal leakage)")

        # 3. Cellular metabolic burden
        burden = self.evaluate_circuit_burden(telem.ribosome_usage_fraction, telem.atp_drain_fraction)
        if burden > self.max_burden_limit:
            anomalies.append(f"Metabolic burden {burden * 100:.1f}% exceeds 30.0% cellular capacity (mutational risk)")

        # 4. Orthogonal host crosstalk
        if telem.host_crosstalk_rate > self.max_crosstalk_limit:
            anomalies.append(f"Host transcriptome crosstalk {telem.host_crosstalk_rate * 100:.1f}% exceeds 5.0% limit")

        # 5. Biosafety & Biocontainment
        if telem.escape_frequency > self.max_escape_freq:
            anomalies.append(f"CRITICAL: Biocontainment escape frequency {telem.escape_frequency:.2e} exceeds 1.0e-8 NIH limit")
        if not telem.auxotrophy_intact:
            anomalies.append("Synthetic auxotrophic nutrient requirement compromised")
        if telem.kill_switch_latency_min > self.max_kill_latency_min:
            anomalies.append(f"Suicide kill-switch latency {telem.kill_switch_latency_min:.1f}min exceeds 60.0min envelope")

        # Biosecurity kill-switch trip condition
        if telem.escape_frequency > 1e-7 or not telem.auxotrophy_intact or burden > 0.45:
            self.is_kill_switch_active = True
            self.kill_reason = "CRITICAL BIOSECURITY TRIP: Triggering Cas3 endonuclease self-destruction"

        return (len(anomalies) == 0, anomalies)

    def trigger_suicide_kill_switch(self) -> Dict[str, str]:
        """Activate redundant genomic self-destruction via MazF toxin and CRISPR-Cas3."""
        self.is_kill_switch_active = True
        return {
            "status": "SUICIDE_KILL_SWITCH_DEPLOYED",
            "mechanism": "DUAL_MAZF_CAS3_GENOME_SHREDDER",
            "target_lysis_time_min": "18.5",
            "chassis_viability": "0.000_PERCENT"
        }
'''
