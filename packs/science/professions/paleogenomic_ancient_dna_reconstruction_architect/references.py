"""Physical references and mathematical models for Paleogenomics & Ancient DNA Reconstruction.

Architect: Dr. Cassian 'The Relic' Sterling
Domain: paleogenomic_ancient_dna_reconstruction_architect
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Quantitative engineering benchmarks for Ancient DNA (aDNA) Reconstruction
MIN_TERMINAL_DEAMINATION_RATE: float = 0.15          # delta_C_to_T >= 0.15 (15% terminal substitution)
MIN_FRAGMENT_LENGTH_BP: float = 30.0                # L_frag >= 30.0 bp
MAX_FRAGMENT_LENGTH_BP: float = 75.0                # L_frag <= 75.0 bp
MAX_MODERN_CONTAMINATION_RATE: float = 0.010        # C_contam <= 0.010 (1.0% max contamination)
MIN_AUTHENTICITY_CONFIDENCE: float = 0.999          # Confidence >= 0.999 (99.9%)
MIN_UDG_REPAIR_EFFICIENCY: float = 0.95             # eta_UDG >= 0.95 (95% repair efficiency)
MIN_SEQUENCING_DEPTH_X: float = 30.0                # Depth >= 30.0x
MIN_PHRED_QUALITY_SCORE: float = 30.0               # Q_Phred >= 30.0 (error <= 1e-3)
MAX_REFERENCE_MAPPING_BIAS: float = 0.020           # Bias_ref <= 0.020 (2.0%)
MIN_DAMAGE_LOG_LIKELIHOOD: float = 10.0             # Lambda_damage >= 10.0


def calculate_briggs_deamination_probability(
    position_from_end: int,
    lambda_param: float = 0.30,
    delta_s: float = 0.28,
    delta_d: float = 0.03
) -> float:
    """Calculate position-dependent C->T deamination probability using the Briggs (2007) model.

    P(C->T | i) = delta_s * (1 - lambda)^(i - 1) + delta_d
    """
    if position_from_end < 1:
        return 0.0

    decay = (1.0 - lambda_param) ** (position_from_end - 1)
    prob = (delta_s * decay) + delta_d
    return max(0.0, min(1.0, prob))


def calculate_fragment_length_density(
    length_bp: float,
    mean_length_bp: float = 48.0
) -> float:
    """Calculate exponential fragmentation probability density for authentic ancient DNA.

    P(L) = (1 / L_mean) * exp(-L / L_mean)
    """
    if length_bp <= 0.0 or mean_length_bp <= 0.0:
        return 0.0

    return (1.0 / mean_length_bp) * math.exp(-length_bp / mean_length_bp)


def calculate_phred_error_probability(phred_score: float) -> float:
    """Calculate base substitution error probability from Phred quality score.

    P_error = 10^(-Q / 10)
    """
    if phred_score <= 0.0:
        return 1.0
    return 10.0 ** (-phred_score / 10.0)


@dataclass
class PaleogenomicValidationResult:
    """Structured validation report for Paleogenomic Ancient DNA parameters."""
    is_valid: bool
    terminal_deamination_rate: float
    mean_fragment_length_bp: float
    modern_contamination_rate: float
    authenticity_confidence: float
    udg_repair_efficiency: float
    sequencing_depth_x: float
    phred_quality_score: float
    reference_mapping_bias: float
    damage_log_likelihood: float
    flaws: List[str]


def validate_paleogenomic_parameters(
    terminal_deamination_rate: float = 0.22,
    mean_fragment_length_bp: float = 48.5,
    modern_contamination_rate: float = 0.005,
    authenticity_confidence: float = 0.9995,
    udg_repair_efficiency: float = 0.97,
    sequencing_depth_x: float = 34.0,
    phred_quality_score: float = 35.0,
    reference_mapping_bias: float = 0.012,
    damage_log_likelihood: float = 14.2
) -> PaleogenomicValidationResult:
    """Validate paleogenomic parameters against Dr. Cassian Sterling's rigorous standards."""
    flaws: List[str] = []

    if terminal_deamination_rate < MIN_TERMINAL_DEAMINATION_RATE:
        flaws.append(
            f"Terminal C->T deamination rate {terminal_deamination_rate:.3f} below ancient authenticity floor "
            f"{MIN_TERMINAL_DEAMINATION_RATE:.2f} (suspected modern DNA contamination)."
        )

    if mean_fragment_length_bp < MIN_FRAGMENT_LENGTH_BP or mean_fragment_length_bp > MAX_FRAGMENT_LENGTH_BP:
        flaws.append(
            f"Mean fragment length {mean_fragment_length_bp:.1f} bp outside ancient fossil bounds "
            f"[{MIN_FRAGMENT_LENGTH_BP:.1f}, {MAX_FRAGMENT_LENGTH_BP:.1f}] bp."
        )

    if modern_contamination_rate > MAX_MODERN_CONTAMINATION_RATE:
        flaws.append(
            f"Modern anthropogenic contamination rate {modern_contamination_rate:.4f} exceeds ceiling "
            f"{MAX_MODERN_CONTAMINATION_RATE:.3f}."
        )

    if authenticity_confidence < MIN_AUTHENTICITY_CONFIDENCE:
        flaws.append(
            f"Paleogenomic authenticity confidence {authenticity_confidence:.4f} below benchmark "
            f"{MIN_AUTHENTICITY_CONFIDENCE:.4f}."
        )

    if udg_repair_efficiency < MIN_UDG_REPAIR_EFFICIENCY:
        flaws.append(
            f"UDG enzymatic repair efficiency {udg_repair_efficiency:.3f} below quality threshold "
            f"{MIN_UDG_REPAIR_EFFICIENCY:.2f}."
        )

    if sequencing_depth_x < MIN_SEQUENCING_DEPTH_X:
        flaws.append(
            f"Paleogenomic sequencing depth {sequencing_depth_x:.1f}x below clinical reconstruction benchmark "
            f"{MIN_SEQUENCING_DEPTH_X:.1f}x."
        )

    if phred_quality_score < MIN_PHRED_QUALITY_SCORE:
        flaws.append(
            f"Phred consensus variant quality score {phred_quality_score:.1f} below minimum Q{MIN_PHRED_QUALITY_SCORE:.0f}."
        )

    if reference_mapping_bias > MAX_REFERENCE_MAPPING_BIAS:
        flaws.append(
            f"Reference genome mapping bias {reference_mapping_bias:.3f} exceeds tolerance "
            f"{MAX_REFERENCE_MAPPING_BIAS:.3f}."
        )

    if damage_log_likelihood < MIN_DAMAGE_LOG_LIKELIHOOD:
        flaws.append(
            f"Damage pattern log-likelihood ratio {damage_log_likelihood:.1f} below authentication threshold "
            f"{MIN_DAMAGE_LOG_LIKELIHOOD:.1f}."
        )

    return PaleogenomicValidationResult(
        is_valid=len(flaws) == 0,
        terminal_deamination_rate=terminal_deamination_rate,
        mean_fragment_length_bp=mean_fragment_length_bp,
        modern_contamination_rate=modern_contamination_rate,
        authenticity_confidence=authenticity_confidence,
        udg_repair_efficiency=udg_repair_efficiency,
        sequencing_depth_x=sequencing_depth_x,
        phred_quality_score=phred_quality_score,
        reference_mapping_bias=reference_mapping_bias,
        damage_log_likelihood=damage_log_likelihood,
        flaws=flaws
    )
