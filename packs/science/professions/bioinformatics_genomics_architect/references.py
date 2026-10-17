"""Computational Genomics & High-Throughput Bioinformatics Architecture Standards.

Author: Dr. Astrid 'The Genome' Vance
Status: Production Reference Standard
"""

import math
import re
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Tuple, Any

# Standard Constants
DEFAULT_REFERENCE_BUILD: str = "GRCh38.p14"
T2T_REFERENCE_BUILD: str = "T2T-CHM13v2.0"
MIN_MAPQ_THRESHOLD: int = 30
MIN_VARIANT_DEPTH_DP: int = 20
MIN_PHRED_QUAL: float = 30.0
MAX_STRAND_BIAS_PVALUE: float = 0.001
SANGER_PHRED_OFFSET: int = 33
MAX_CALPHA_CONTACT_ANGSTROM: float = 8.0

CIGAR_TOKEN_REGEX = re.compile(r"^(\d+[MIDNSHP=X])+$")
CIGAR_OPERATION_REGEX = re.compile(r"(\d+)([MIDNSHP=X])")


@dataclass(frozen=True)
class FastqRecord:
    """Represents a single high-throughput sequencing read in FASTQ format."""
    header: str
    sequence: str
    quality: str

    def to_phred_scores(self, offset: int = SANGER_PHRED_OFFSET) -> List[int]:
        """Convert ASCII quality characters to Phred quality integer scores."""
        return [ord(char) - offset for char in self.quality]

    def mean_quality(self, offset: int = SANGER_PHRED_OFFSET) -> float:
        """Compute the arithmetic mean Phred quality score."""
        scores = self.to_phred_scores(offset=offset)
        if not scores:
            return 0.0
        return sum(scores) / len(scores)

    def error_probability(self, offset: int = SANGER_PHRED_OFFSET) -> List[float]:
        """Convert Phred quality scores into base error probabilities P = 10^(-Q/10)."""
        return [10.0 ** (-score / 10.0) for score in self.to_phred_scores(offset=offset)]


class FastqStreamParser:
    """O(1) memory generator parser for multi-gigabyte FASTQ sequences."""

    @staticmethod
    def parse_stream(lines: Iterator[str]) -> Iterator[FastqRecord]:
        """Stream reads one by one without buffering entire files in memory."""
        line_num = 0
        header = ""
        sequence = ""
        plus_marker = ""

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            state = line_num % 4
            if state == 0:
                if not line.startswith("@"):
                    raise ValueError(f"Malformed FASTQ header at record line {line_num + 1}: expected '@'")
                header = line[1:]
            elif state == 1:
                sequence = line.upper()
            elif state == 2:
                if not line.startswith("+"):
                    raise ValueError(f"Malformed FASTQ plus line at record line {line_num + 1}: expected '+'")
                plus_marker = line
            elif state == 3:
                quality = line
                if len(sequence) != len(quality):
                    raise ValueError(
                        f"Sequence length ({len(sequence)}) does not match quality length ({len(quality)}) at {header}"
                    )
                yield FastqRecord(header=header, sequence=sequence, quality=quality)

            line_num += 1


class CigarParser:
    """Validates and parses SAM/BAM CIGAR alignment operation strings."""

    @staticmethod
    def validate_syntax(cigar_str: str) -> bool:
        """Verify whether the CIGAR string strictly adheres to SAMv1 specification."""
        if not cigar_str or cigar_str == "*":
            return False
        return bool(CIGAR_TOKEN_REGEX.fullmatch(cigar_str))

    @staticmethod
    def parse_operations(cigar_str: str) -> List[Tuple[int, str]]:
        """Parse CIGAR string into list of (length, operation) tuples."""
        if not CigarParser.validate_syntax(cigar_str):
            raise ValueError(f"Invalid CIGAR string: '{cigar_str}' does not match standard grammar")
        matches = CIGAR_OPERATION_REGEX.findall(cigar_str)
        return [(int(length), op) for length, op in matches]

    @staticmethod
    def alignment_reference_span(cigar_str: str) -> int:
        """Compute the length on the reference spanned by the alignment (M, D, N, =, X)."""
        ops = CigarParser.parse_operations(cigar_str)
        span = 0
        for length, op in ops:
            if op in {"M", "D", "N", "=", "X"}:
                span += length
        return span


@dataclass
class SamAlignment:
    """Represents a coordinate-aligned sequencing read from a SAM/BAM file."""
    qname: str
    flag: int
    rname: str
    pos: int
    mapq: int
    cigar: str
    seq: str
    qual: str

    def is_mapped(self) -> bool:
        """Check if read is unmapped according to bit flag 0x4."""
        return not bool(self.flag & 0x4)

    def is_high_confidence(self, min_mapq: int = MIN_MAPQ_THRESHOLD) -> bool:
        """Verify if alignment mapping quality meets high-confidence threshold."""
        return self.is_mapped() and self.mapq >= min_mapq

    def reference_span(self) -> int:
        """Get aligned span on reference sequence."""
        if not self.is_mapped() or self.cigar == "*":
            return 0
        return CigarParser.alignment_reference_span(self.cigar)


@dataclass
class VcfVariant:
    """Represents a candidate genetic variant record in VCF 4.2/4.3 specification."""
    chrom: str
    pos: int
    variant_id: str
    ref: str
    alt: str
    qual: float
    filter_status: str
    info: Dict[str, Any] = field(default_factory=dict)

    def get_depth(self) -> int:
        """Extract total sequencing depth DP from INFO dictionary."""
        val = self.info.get("DP", 0)
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    def get_strand_bias_pvalue(self) -> float:
        """Extract Fisher strand bias p-value (FS or SP) from INFO dictionary."""
        val = self.info.get("SP_PVAL", 1.0)
        try:
            return float(val)
        except (ValueError, TypeError):
            return 1.0

    def get_allele_frequency(self) -> float:
        """Extract alternative allele frequency AF from INFO dictionary."""
        val = self.info.get("AF", 0.0)
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    def passes_clinical_qc(
        self,
        min_depth: int = MIN_VARIANT_DEPTH_DP,
        min_qual: float = MIN_PHRED_QUAL,
        max_strand_bias_p: float = MAX_STRAND_BIAS_PVALUE,
    ) -> Tuple[bool, List[str]]:
        """Validate variant against clinical quality criteria."""
        failures = []
        dp = self.get_depth()
        if dp < min_depth:
            failures.append(f"LowDepth: DP={dp} < {min_depth}")
        if self.qual < min_qual:
            failures.append(f"LowQual: QUAL={self.qual:.1f} < {min_qual}")
        sb = self.get_strand_bias_pvalue()
        if sb < max_strand_bias_p:
            failures.append(f"StrandBias: p={sb:.5f} < {max_strand_bias_p}")
        return len(failures) == 0, failures


@dataclass(frozen=True)
class ProteinResidue:
    """3D Cartesian coordinate representation of an alpha-carbon atom in a protein backbone."""
    residue_id: int
    residue_name: str
    x: float
    y: float
    z: float

    def distance_to(self, other: "ProteinResidue") -> float:
        """Compute Euclidean distance in Angstroms to another C-alpha residue."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)


class ProteinContactMap:
    """Residue-residue structural contact map computer."""

    @staticmethod
    def compute_contacts(
        residues: List[ProteinResidue], cutoff_angstrom: float = MAX_CALPHA_CONTACT_ANGSTROM
    ) -> List[Tuple[int, int, float]]:
        """Compute all non-adjacent residue pairs within physical contact distance."""
        contacts = []
        n = len(residues)
        for i in range(n):
            for j in range(i + 2, n):  # Exclude immediate sequence neighbors
                dist = residues[i].distance_to(residues[j])
                if dist <= cutoff_angstrom:
                    contacts.append((residues[i].residue_id, residues[j].residue_id, dist))
        return contacts


class BioinformaticsReferenceLibrary:
    """Canonical repository of high-throughput genomics engineering standards."""

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        return {
            "default_assembly": DEFAULT_REFERENCE_BUILD,
            "min_mapq": MIN_MAPQ_THRESHOLD,
            "min_variant_depth": MIN_VARIANT_DEPTH_DP,
            "min_phred_qual": MIN_PHRED_QUAL,
            "max_strand_bias_pval": MAX_STRAND_BIAS_PVALUE,
            "sanger_phred_offset": SANGER_PHRED_OFFSET,
            "calpha_contact_distance_angstrom": MAX_CALPHA_CONTACT_ANGSTROM,
        }

    @staticmethod
    def get_anti_patterns() -> List[str]:
        return [
            "Calling .read() or .readlines() on multi-gigabyte FASTQ/BAM files causing heap OOM",
            "Accepting variant calls with depth DP < 20 or Phred QUAL < 30 without quality filter tagging",
            "Parsing CIGAR strings without regex/grammar validation causing misaligned coordinate offsets",
            "Stochastic pipelines without fixed random seeds or pinned reference genome assembly hashes",
            "Mixing Phred+33 Sanger offsets with Phred+64 Illumina legacy offsets",
            "Calculating contact maps without Euclidean 3D distance bounds validation",
        ]

    @staticmethod
    def get_reproducibility_checklist() -> List[str]:
        return [
            "Pin exact reference genome build (e.g. GRCh38.p14) with SHA-256 digest",
            "Set explicit random seeds (e.g. seed=42) for stochastic variant callers or aligners",
            "Use generator/streaming parsing for all high-throughput sequence formats",
            "Filter variant calls against minimum depth (DP >= 20) and quality (QUAL >= 30)",
            "Validate all CIGAR tokens against standard SAMv1 grammar",
            "Record execution environment, tool versions, and command lineage in headers",
        ]

    @staticmethod
    def get_canonical_core() -> str:
        return r'''"""Canonical High-Throughput Computational Genomics Engine.
Reference: GRCh38.p14 / T2T-CHM13v2.0
"""

import math
import re
from typing import Iterator, Dict, Any, List, Tuple

REFERENCE_BUILD = "GRCh38.p14"
RANDOM_SEED = 42

class FastqStreamParser:
    """O(1) memory generator parser for multi-gigabyte FASTQ sequences."""

    @staticmethod
    def parse_stream(lines: Iterator[str]) -> Iterator[Dict[str, Any]]:
        line_num = 0
        header, sequence = "", ""
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            state = line_num % 4
            if state == 0 and line.startswith("@"):
                header = line[1:]
            elif state == 1:
                sequence = line.upper()
            elif state == 3:
                yield {"header": header, "sequence": sequence, "quality": line}
            line_num += 1

class CigarParser:
    """Validates and parses SAM/BAM CIGAR alignment operation strings."""
    CIGAR_TOKEN_REGEX = re.compile(r"^(\d+[MIDNSHP=X])+$")
    CIGAR_OPERATION_REGEX = re.compile(r"(\d+)([MIDNSHP=X])")

    @classmethod
    def validate_syntax(cls, cigar_str: str) -> bool:
        if not cigar_str or cigar_str == "*":
            return False
        return bool(cls.CIGAR_TOKEN_REGEX.fullmatch(cigar_str))

    @classmethod
    def parse_operations(cls, cigar_str: str) -> List[Tuple[int, str]]:
        if not cls.validate_syntax(cigar_str):
            raise ValueError(f"Invalid CIGAR: '{cigar_str}'")
        return [(int(length), op) for length, op in cls.CIGAR_OPERATION_REGEX.findall(cigar_str)]

def filter_high_confidence_alignments(alignments: List[Dict[str, Any]], min_mapq: int = 30) -> List[Dict[str, Any]]:
    return [
        aln for aln in alignments
        if aln.get("mapq", 0) >= min_mapq and CigarParser.validate_syntax(aln.get("cigar", ""))
    ]

def filter_clinical_variants(
    variants: List[Dict[str, Any]],
    min_depth: int = 20,
    min_qual: float = 30.0,
    max_strand_bias: float = 0.001
) -> List[Dict[str, Any]]:
    passed_variants = []
    for var in variants:
        dp = var.get("DP", 0)
        qual = var.get("QUAL", 0.0)
        strand_bias = var.get("SP_PVAL", 1.0)
        if dp >= min_depth and qual >= min_qual and strand_bias >= max_strand_bias:
            passed_variants.append(var)
    return passed_variants

class ProteinContactMap:
    """Computes residue contact networks based on C-alpha Euclidean distances."""

    @staticmethod
    def compute_contacts(residues: List[Dict[str, Any]], cutoff_angstrom: float = 8.0) -> List[Tuple[int, int, float]]:
        contacts = []
        n = len(residues)
        for i in range(n):
            for j in range(i + 2, n):
                r1, r2 = residues[i], residues[j]
                dist = math.sqrt((r1["x"] - r2["x"])**2 + (r1["y"] - r2["y"])**2 + (r1["z"] - r2["z"])**2)
                if dist <= cutoff_angstrom:
                    contacts.append((r1["id"], r2["id"], dist))
        return contacts
'''

