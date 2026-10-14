"""
Diana Drake's Linguistic & Conversion Copywriting Inspector
Deep empirical measurement engine for Flesch reading ease, AI cliche eradication,
customer-centricity ("You" vs "We" ratio), and high-intent CTA psychology.
"""

import os
import re
from typing import Dict, Any, List, Tuple, Optional


def count_syllables(word: str) -> int:
    """Estimates syllables in an English word using phonetic regex."""
    w = word.lower().strip()
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]|ed|es|e)$", "", w)
    w = re.sub(r"^y", "", w)
    syllables = len(re.findall(r"[aeiouy]{1,2}", w))
    return max(1, syllables)


class DianaCopywritingInspector:
    """Diana Drake's Linguistic & Persuasion Inspection Engine."""

    AI_CLICHES = [
        r"\bwelcome to\b",
        r"\bin today's (?:fast-paced|digital|modern|interconnected) world\b",
        r"\brevolutionize\b",
        r"\bseamlessly\b",
        r"\bempower(?:ing|s)?\b",
        r"\bcutting-edge\b",
        r"\bgame-changer\b",
        r"\bdive in\b",
        r"\blook no further\b",
        r"\bunlock your potential\b",
        r"\bat your fingertips\b",
        r"\bharness the power\b",
        r"\bdelve into\b"
    ]

    PASSIVE_CTAS = [
        r"\bclick here\b",
        r"\blearn more\b",
        r"\bsubmit\b",
        r"\bread more\b",
        r"\bcontinue\b"
    ]

    def __init__(self, target_file: str):
        self.target_file = os.path.abspath(target_file)

    def inspect(self) -> Dict[str, Any]:
        """
        Executes an objective, deep copywriting inspection:
        - Flesch Reading Ease score
        - Average words per sentence
        - AI Cliche & Corporate Jargon matches
        - "You" vs "We" customer-centric ratio
        - Passive vs High-Intent CTA audit
        - Headline hook evaluation
        """
        metrics: Dict[str, Any] = {
            "target": self.target_file,
            "word_count": 0,
            "sentence_count": 0,
            "avg_words_per_sentence": 0.0,
            "flesch_reading_ease": 70.0,
            "you_count": 0,
            "we_count": 0,
            "you_to_we_ratio": 2.0,
            "ai_cliches_found": [],
            "passive_ctas_found": [],
            "h1_text": "",
            "has_weak_h1": False
        }

        if not os.path.exists(self.target_file):
            metrics["error"] = f"File {self.target_file} does not exist"
            return metrics

        try:
            with open(self.target_file, "r", encoding="utf-8", errors="ignore") as f:
                raw_content = f.read()

            # 1. Extract visible text (strip scripts and styles)
            clean_text = re.sub(r"<script[^>]*>[\s\S]*?</script>", " ", raw_content, flags=re.IGNORECASE)
            clean_text = re.sub(r"<style[^>]*>[\s\S]*?</style>", " ", clean_text, flags=re.IGNORECASE)
            clean_text = re.sub(r"<[^>]+>", " ", clean_text)
            clean_text = " ".join(clean_text.split())

            # 2. Extract H1 text
            h1_match = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", raw_content, re.IGNORECASE)
            if h1_match:
                h1_raw = re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()
                metrics["h1_text"] = h1_raw
                # Check weak H1
                words = h1_raw.split()
                metrics["has_weak_h1"] = (len(words) <= 3 or "welcome" in h1_raw.lower() or "home" in h1_raw.lower())

            # 3. Sentences & Words
            sentences = [s.strip() for s in re.split(r"[.!?]+", clean_text) if len(s.strip()) > 2]
            words = [w.strip() for w in re.findall(r"\b[A-Za-z0-9'-]+\b", clean_text) if len(w) > 0]

            total_words = len(words)
            total_sentences = max(1, len(sentences))

            metrics["word_count"] = total_words
            metrics["sentence_count"] = total_sentences

            if total_words > 0:
                avg_words = round(total_words / total_sentences, 1)
                metrics["avg_words_per_sentence"] = avg_words

                total_syllables = sum(count_syllables(w) for w in words)
                # Flesch Reading Ease Formula
                flesch = 206.835 - (1.015 * (total_words / total_sentences)) - (84.6 * (total_syllables / total_words))
                metrics["flesch_reading_ease"] = round(max(0.0, min(100.0, flesch)), 1)

            # 4. "You" vs "We" Customer-Centric Ratio
            you_hits = len(re.findall(r"\b(you|your|yours|yourself)\b", clean_text, re.IGNORECASE))
            we_hits = len(re.findall(r"\b(we|our|ours|us|i|my|mine)\b", clean_text, re.IGNORECASE))
            metrics["you_count"] = you_hits
            metrics["we_count"] = we_hits
            metrics["you_to_we_ratio"] = round(you_hits / max(1, we_hits), 2)

            # 5. AI Cliches detection
            cliches_found = []
            for pattern in self.AI_CLICHES:
                found = re.findall(pattern, clean_text, re.IGNORECASE)
                if found:
                    cliches_found.extend([f.lower() for f in found])
            metrics["ai_cliches_found"] = list(set(cliches_found))

            # 6. Passive CTAs detection
            passive_ctas = []
            for pattern in self.PASSIVE_CTAS:
                found = re.findall(pattern, raw_content, re.IGNORECASE)
                if found:
                    passive_ctas.extend([f.lower() for f in found])
            metrics["passive_ctas_found"] = list(set(passive_ctas))

        except Exception as e:
            metrics["inspection_error"] = str(e)

        return metrics
