"""
Damian Vance - Principal Interactive Audio & Sound Architect Master Subsystem.
"""

from professions.audio_sound_architect.references import (
    AudioReferenceLibrary,
    AUDIO_SYSTEM_BENCHMARKS,
    ADSR_ENVELOPE_PROFILES,
    SPATIAL_ACOUSTIC_DEFAULTS,
    TOXIC_AUDIO_ANTI_PATTERNS,
    CANONICAL_WEB_AUDIO_CORE,
)
from professions.audio_sound_architect.inspector import (
    AudioSystemInspector,
    AudioMetrics,
    AudioInspectionReport,
)
from professions.audio_sound_architect.rubric import (
    AudioArchitectureRubric,
    AudioRubricEvaluation,
)
from professions.audio_sound_architect.blind_critic import (
    BlindAudioCritic,
    AudioDefect,
    AudioDefectLedger,
)
from professions.audio_sound_architect.elevation_engine import AudioElevationEngine
from professions.audio_sound_architect.master import DamianVanceMaster

__all__ = [
    "AudioReferenceLibrary",
    "AUDIO_SYSTEM_BENCHMARKS",
    "ADSR_ENVELOPE_PROFILES",
    "SPATIAL_ACOUSTIC_DEFAULTS",
    "TOXIC_AUDIO_ANTI_PATTERNS",
    "CANONICAL_WEB_AUDIO_CORE",
    "AudioSystemInspector",
    "AudioMetrics",
    "AudioInspectionReport",
    "AudioArchitectureRubric",
    "AudioRubricEvaluation",
    "BlindAudioCritic",
    "AudioDefect",
    "AudioDefectLedger",
    "AudioElevationEngine",
    "DamianVanceMaster",
]
