"""
Diana Drake's Empirical Conversion Copywriting Benchmarks
Quantitative linguistic standards derived from Direct-Response Marketing (Eugene Schwartz, Gary Halbert) and Apple/Stripe copy.
Measures readability, customer-centricity ("You" vs "We"), CTA intent velocity, and zero AI cliches.
"""

from typing import Dict, Any, List


class DianaCopywritingReferences:
    """Diana Drake's Curated Empirical Copywriting Benchmarks."""

    BENCHMARK_PROFILES: Dict[str, Dict[str, Any]] = {
        "saas_high_converting_landing": {
            "name": "High-Converting SaaS Landing Page",
            "description": "Clear value proposition, punchy benefits, high reading ease, zero corporate AI fluff.",
            "metrics": {
                "min_flesch_reading_ease": 60.0,
                "max_avg_sentence_words": 18,
                "max_allowed_ai_cliches": 0,
                "min_you_to_we_ratio": 1.5,
                "requires_high_intent_cta": True,
                "forbid_passive_submit_buttons": True
            }
        },
        "direct_response_sales_letter": {
            "name": "Direct-Response Sales Copy",
            "description": "Conversational urgency, emotional resonance, extreme reader focus, high hook velocity.",
            "metrics": {
                "min_flesch_reading_ease": 65.0,
                "max_avg_sentence_words": 15,
                "max_allowed_ai_cliches": 0,
                "min_you_to_we_ratio": 2.0,
                "requires_high_intent_cta": True,
                "forbid_passive_submit_buttons": True
            }
        },
        "microcopy_product_onboarding": {
            "name": "Product UX Microcopy & Onboarding",
            "description": "Frictionless, concise UI text guiding user to first value moment without cognitive drag.",
            "metrics": {
                "min_flesch_reading_ease": 70.0,
                "max_avg_sentence_words": 10,
                "max_allowed_ai_cliches": 0,
                "min_you_to_we_ratio": 1.8,
                "requires_high_intent_cta": True,
                "forbid_passive_submit_buttons": True
            }
        }
    }

    def __init__(self, profile_name: str = "saas_high_converting_landing"):
        self.profile_name = profile_name
        self.active_profile = self.BENCHMARK_PROFILES.get(
            profile_name,
            self.BENCHMARK_PROFILES["saas_high_converting_landing"]
        )

    def get_benchmarks(self) -> Dict[str, Any]:
        """Returns the active quantitative benchmark profile."""
        return self.active_profile

    def get_available_profiles(self) -> List[str]:
        """Lists all copywriting profiles known to Diana."""
        return list(self.BENCHMARK_PROFILES.keys())
