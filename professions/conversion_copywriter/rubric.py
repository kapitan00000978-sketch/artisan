"""
Diana Drake's Weighted Conversion Copywriting Rubric
Mathematical, psychological evaluation of reading ease, hook strength, zero AI cliches, and CTA intent velocity.
"""

from typing import Dict, Any, List, Optional


class DianaCopywritingRubric:
    """Diana Drake's 100-point weighted conversion copywriting evaluation rubric."""

    DIMENSIONS: Dict[str, Dict[str, Any]] = {
        "flesch_reading_ease": {
            "title": "Flesch Reading Ease & Scannability",
            "weight": 0.25,
            "benchmark": "Reading Ease score >= 60.0; avg sentence length <= 18 words."
        },
        "headline_hook_power": {
            "title": "Headline Hook & Value Proposition",
            "weight": 0.25,
            "benchmark": "Specific outcome-focused promise; rejects generic 1-3 word labels or 'Welcome' headers."
        },
        "ai_cliche_purity": {
            "title": "Zero AI Cliches & Jargon Purity",
            "weight": 0.20,
            "benchmark": "Zero corporate filler phrases ('in today's digital world', 'seamlessly revolutionize')."
        },
        "cta_action_psychology": {
            "title": "CTA Action Psychology & Velocity",
            "weight": 0.15,
            "benchmark": "High-intent action verbs (Start, Claim, Launch); zero passive 'Click here' or 'Learn more'."
        },
        "customer_centricity": {
            "title": "Customer-Centricity ('You' vs 'We' Ratio)",
            "weight": 0.15,
            "benchmark": "'You' to 'We' pronoun ratio >= 1.5; reader-focused benefits rather than brand ego."
        }
    }

    def evaluate(self, metrics: Dict[str, Any], benchmark_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates itemized and composite copywriting score out of 100."""
        target_metrics = benchmark_profile.get("metrics", {}) if benchmark_profile else {}
        min_flesch = target_metrics.get("min_flesch_reading_ease", 60.0)
        min_ratio = target_metrics.get("min_you_to_we_ratio", 1.5)

        scores: Dict[str, Any] = {}

        # 1. Flesch Reading Ease (0-10)
        flesch = metrics.get("flesch_reading_ease", 70.0)
        avg_words = metrics.get("avg_words_per_sentence", 15.0)

        if flesch >= min_flesch and avg_words <= 18.0:
            f_score = 10.0
        elif flesch >= min_flesch - 10:
            f_score = 8.0
        elif flesch >= 40.0:
            f_score = 5.5
        else:
            f_score = 3.0

        scores["flesch_reading_ease"] = {
            "score": f_score,
            "measured": f"Flesch: {flesch}/100 (Avg words/sentence: {avg_words})",
            "benchmark": f">= {min_flesch} Reading Ease",
            "status": "PASS" if f_score >= 8.0 else "FAIL"
        }

        # 2. Headline Hook Power (0-10)
        h1 = metrics.get("h1_text", "")
        weak_h1 = metrics.get("has_weak_h1", False)

        if h1 and not weak_h1:
            h_score = 10.0
        elif not h1:
            h_score = 4.0
        else:
            h_score = 3.0

        scores["headline_hook_power"] = {
            "score": h_score,
            "measured": f"H1: '{h1}'" if h1 else "Missing H1 headline",
            "benchmark": "Specific, outcome-driven hook without generic labels",
            "status": "PASS" if h_score >= 8.0 else "FAIL"
        }

        # 3. AI Cliche Purity (0-10)
        cliches = metrics.get("ai_cliches_found", [])
        if len(cliches) == 0:
            c_score = 10.0
        elif len(cliches) == 1:
            c_score = 5.0
        else:
            c_score = 1.0

        scores["ai_cliche_purity"] = {
            "score": c_score,
            "measured": f"{len(cliches)} cliches found: {', '.join(cliches)}" if cliches else "Zero AI cliches",
            "benchmark": "Zero AI or corporate cliches",
            "status": "PASS" if c_score >= 8.0 else "FAIL"
        }

        # 4. CTA Action Psychology (0-10)
        passive_ctas = metrics.get("passive_ctas_found", [])
        if len(passive_ctas) == 0:
            cta_score = 10.0
        elif len(passive_ctas) == 1:
            cta_score = 5.0
        else:
            cta_score = 2.0

        scores["cta_action_psychology"] = {
            "score": cta_score,
            "measured": f"{len(passive_ctas)} passive CTA(s): {', '.join(passive_ctas)}" if passive_ctas else "High-intent action triggers certified",
            "benchmark": "Zero passive 'Click here' or 'Learn more' buttons",
            "status": "PASS" if cta_score >= 8.0 else "FAIL"
        }

        # 5. Customer-Centricity (0-10)
        ratio = metrics.get("you_to_we_ratio", 2.0)
        if ratio >= min_ratio:
            ratio_score = 10.0
        elif ratio >= 1.0:
            ratio_score = 7.5
        elif ratio >= 0.5:
            ratio_score = 5.0
        else:
            ratio_score = 2.5

        scores["customer_centricity"] = {
            "score": ratio_score,
            "measured": f"You/We ratio: {ratio} (You: {metrics.get('you_count')}, We: {metrics.get('we_count')})",
            "benchmark": f">= {min_ratio} ratio",
            "status": "PASS" if ratio_score >= 8.0 else "FAIL"
        }

        # Weighted calculation
        total_score = round(sum(
            scores[dim]["score"] * self.DIMENSIONS[dim]["weight"]
            for dim in self.DIMENSIONS
        ) * 10, 1)

        return {
            "evaluator": "Diana Drake (Direct-Response Copywriter)",
            "total_score": total_score,
            "passing_threshold": 85.0,
            "passed": total_score >= 85.0,
            "dimensions": scores
        }
