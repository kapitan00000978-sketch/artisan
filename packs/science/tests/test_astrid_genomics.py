"""Unit tests for Dr. Astrid 'The Genome' Vance — Computational Genomics & Bioinformatics Master.

Validates the complete 7-step autonomous craftsmanship standard for Domain Master #26.
"""

import pytest
from professions.bioinformatics_genomics_architect.references import (
    BioinformaticsReferenceLibrary,
    FastqRecord,
    FastqStreamParser,
    CigarParser,
    SamAlignment,
    VcfVariant,
    ProteinResidue,
    ProteinContactMap,
    DEFAULT_REFERENCE_BUILD,
    MIN_MAPQ_THRESHOLD,
    MIN_VARIANT_DEPTH_DP,
    MIN_PHRED_QUAL,
)
from professions.bioinformatics_genomics_architect.inspector import BioinformaticsInspector
from professions.bioinformatics_genomics_architect.rubric import BioinformaticsRubric
from professions.bioinformatics_genomics_architect.blind_critic import BioinformaticsBlindCritic
from professions.bioinformatics_genomics_architect.elevation_engine import BioinformaticsElevationEngine
from professions.bioinformatics_genomics_architect.master import AstridVanceMaster


def test_fastq_record_and_phred_math():
    """Validates FastqRecord Phred score calculations and base error probabilities."""
    # ASCII 'I' has ord 73 -> Phred score 40 (Q40 = 99.99% accuracy)
    # ASCII '?' has ord 63 -> Phred score 30 (Q30 = 99.9% accuracy)
    rec = FastqRecord(
        header="READ_001",
        sequence="ACGT",
        quality="II??"
    )
    scores = rec.to_phred_scores(offset=33)
    assert scores == [40, 40, 30, 30]
    assert rec.mean_quality(offset=33) == 35.0

    probs = rec.error_probability(offset=33)
    assert len(probs) == 4
    assert pytest.approx(probs[0], rel=1e-3) == 0.0001
    assert pytest.approx(probs[2], rel=1e-3) == 0.001


def test_fastq_stream_parser_generator():
    """Validates streaming generator parsing of FASTQ records with constant memory."""
    raw_lines = [
        "@READ_1\n",
        "ACGTACGT\n",
        "+READ_1\n",
        "IIII????\n",
        "@READ_2\n",
        "TGCATGCA\n",
        "+\n",
        "JJJJIIII\n",
    ]
    parser = FastqStreamParser.parse_stream(iter(raw_lines))
    records = list(parser)

    assert len(records) == 2
    assert records[0].header == "READ_1"
    assert records[0].sequence == "ACGTACGT"
    assert records[1].header == "READ_2"
    assert records[1].sequence == "TGCATGCA"

    # Test malformed header error handling
    bad_lines = ["NOT_A_HEADER\n", "ACGT\n", "+\n", "IIII\n"]
    with pytest.raises(ValueError, match="Malformed FASTQ header"):
        list(FastqStreamParser.parse_stream(iter(bad_lines)))


def test_cigar_parser_syntax_and_span():
    """Validates CIGAR syntax validation, operation extraction, and reference alignment span."""
    valid_cigar = "50M2D10M"
    assert CigarParser.validate_syntax(valid_cigar) is True
    ops = CigarParser.parse_operations(valid_cigar)
    assert ops == [(50, "M"), (2, "D"), (10, "M")]
    # Span on reference is 50 + 2 + 10 = 62
    assert CigarParser.alignment_reference_span(valid_cigar) == 62

    invalid_cigar = "50M?10X"
    assert CigarParser.validate_syntax(invalid_cigar) is False
    with pytest.raises(ValueError, match="Invalid CIGAR"):
        CigarParser.parse_operations(invalid_cigar)

    sam = SamAlignment(
        qname="READ_SAM_1",
        flag=0,
        rname="chr1",
        pos=1000,
        mapq=42,
        cigar="100M",
        seq="A" * 100,
        qual="I" * 100,
    )
    assert sam.is_mapped() is True
    assert sam.is_high_confidence(min_mapq=30) is True
    assert sam.reference_span() == 100


def test_vcf_variant_filtering_and_qc():
    """Validates clinical variant depth, Phred quality, and strand bias filtering."""
    good_variant = VcfVariant(
        chrom="chr7",
        pos=140453136,
        variant_id="rs121913342",
        ref="A",
        alt="T",
        qual=99.0,
        filter_status="PASS",
        info={"DP": 45, "AF": 0.5, "SP_PVAL": 0.25},
    )
    passed, failures = good_variant.passes_clinical_qc()
    assert passed is True
    assert len(failures) == 0

    bad_variant = VcfVariant(
        chrom="chr7",
        pos=140453136,
        variant_id=".",
        ref="A",
        alt="T",
        qual=15.0,  # Below 30.0 threshold
        filter_status="LowQual",
        info={"DP": 8, "SP_PVAL": 0.00001},  # Below DP 20 and severe strand bias
    )
    passed, failures = bad_variant.passes_clinical_qc()
    assert passed is False
    assert any("LowDepth" in f for f in failures)
    assert any("LowQual" in f for f in failures)
    assert any("StrandBias" in f for f in failures)


def test_protein_contact_map_euclidean():
    """Validates 3D Euclidean residue distance contact map calculations."""
    r1 = ProteinResidue(residue_id=1, residue_name="ALA", x=0.0, y=0.0, z=0.0)
    r2 = ProteinResidue(residue_id=2, residue_name="GLY", x=1.0, y=1.0, z=1.0)
    r3 = ProteinResidue(residue_id=3, residue_name="LEU", x=3.0, y=4.0, z=0.0)  # dist from r1 is 5.0 Å
    r4 = ProteinResidue(residue_id=4, residue_name="TRP", x=20.0, y=20.0, z=20.0)  # far away

    dist_1_3 = r1.distance_to(r3)
    assert pytest.approx(dist_1_3, rel=1e-3) == 5.0

    contacts = ProteinContactMap.compute_contacts([r1, r2, r3, r4], cutoff_angstrom=8.0)
    # Contact between r1 and r3 (non-adjacent, distance 5.0 <= 8.0)
    assert (1, 3, 5.0) in contacts
    # r4 is distant, should not be in contacts
    assert not any(c[0] == 4 or c[1] == 4 for c in contacts)


def test_inspector_and_rubric():
    """Validates code inspection, comment stripping, and 100-point rubric with veto accumulation."""
    clean_code = BioinformaticsReferenceLibrary.get_canonical_core()
    metrics = BioinformaticsInspector.inspect(clean_code)

    assert metrics["ast_valid"] is True
    assert metrics["has_streaming_parser"] is True
    assert metrics["has_whole_file_slurp"] is False
    assert metrics["has_cigar_logic"] is True
    assert metrics["has_reference_provenance"] is True
    assert metrics["has_proteomic_structure"] is True

    score, breakdown, passed, veto_reason = BioinformaticsRubric.evaluate(metrics)
    assert score >= 85
    assert passed is True
    assert veto_reason == ""

    # Test veto on lazy stubs and whole-file slurp
    bad_code = "data = open('genome.fastq').read() # TODO: fix later"
    bad_metrics = BioinformaticsInspector.inspect(bad_code)
    bad_score, _, bad_passed, bad_veto = BioinformaticsRubric.evaluate(bad_metrics)
    assert bad_passed is False
    assert "CraftsmanshipDefect" in bad_veto or "MemoryOOMHazard" in bad_veto


def test_blind_critic_and_elevation_master():
    """Validates blind critique, closed-loop elevation, and AstridVanceMaster full cycle."""
    flawed_code = '''
def process_genomics(filename):
    data = open(filename).read()
    # TODO: add variant filter
    return data
'''
    critic_report = BioinformaticsBlindCritic.evaluate(flawed_code)
    assert critic_report["verdict"] == "REJECTED"
    assert critic_report["fatal_defects_count"] > 0

    elevation = BioinformaticsElevationEngine.elevate(flawed_code, target_score=85)
    assert elevation["passed"] is True
    assert elevation["final_score"] >= 85
    assert "FastqStreamParser" in elevation["elevated_code"]

    # Test master autonomous cycle with default canonical core
    master = AstridVanceMaster()
    result = master.run_autonomous_cycle()

    assert result["status"] == "CERTIFIED"
    assert result["is_certified"] is True
    assert result["final_score"] >= 85
    assert result["verdict"] == "APPROVED"
    assert "EXECUTIVE BIOINFORMATICS BRIEFING" in result["executive_briefing"]
