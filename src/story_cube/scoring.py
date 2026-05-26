from __future__ import annotations

import re
from collections import defaultdict
from statistics import mean

from .models import ContributionScore, StoryContribution


DIMENSIONS = (
    "creativity",
    "technical_coherence",
    "inclusivity_awareness",
    "collaboration",
)


def _clamp(value: float, min_value: float = 0.0, max_value: float = 5.0) -> float:
    return max(min_value, min(max_value, round(value, 2)))


def score_contribution(
    text: str,
    rolled_face_labels: list[str],
    referenced_player_ids: list[str] | None = None,
    included_quiet_player: bool = False,
) -> ContributionScore:
    referenced_player_ids = referenced_player_ids or []
    lower = text.lower()
    words = re.findall(r"\b[a-zA-Z]{3,}\b", lower)

    creativity = 1.0
    if len(set(words)) >= 20:
        creativity += 1.0
    if any(token in lower for token in ("imagine", "unexpected", "new", "alternative", "scenario")):
        creativity += 1.0
    if text.count("?") >= 1 or text.count("!") >= 1:
        creativity += 0.5

    technical = 1.0
    technical_tokens = (
        "adf",
        "pipeline",
        "databricks",
        "delta",
        "ingestion",
        "orchestration",
        "monitoring",
        "quality",
        "lineage",
        "governance",
    )
    technical += min(2.5, 0.5 * sum(1 for token in technical_tokens if token in lower))
    if any(face.lower() in lower for face in rolled_face_labels):
        technical += 1.0

    inclusivity = 1.0
    inclusion_tokens = (
        "inclusion",
        "inclusive",
        "accessibility",
        "bias",
        "fair",
        "equity",
        "diverse",
        "representation",
        "language",
        "people",
    )
    inclusivity += min(3.0, 0.5 * sum(1 for token in inclusion_tokens if token in lower))
    if any(token in lower for token in ("underrepresented", "quiet", "voice", "safe")):
        inclusivity += 0.5

    collaboration = 1.0
    if referenced_player_ids:
        collaboration += min(2.0, 0.6 * len(set(referenced_player_ids)))
    if any(token in lower for token in ("building on", "as mentioned", "continuing", "together", "we")):
        collaboration += 1.0
    if included_quiet_player:
        collaboration += 1.0

    return ContributionScore(
        creativity=_clamp(creativity),
        technical_coherence=_clamp(technical),
        inclusivity_awareness=_clamp(inclusivity),
        collaboration=_clamp(collaboration),
    )


def aggregate_player_dimension_averages(contributions: list[StoryContribution]) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for contribution in contributions:
        if not contribution.score:
            continue
        grouped[contribution.player_id]["creativity"].append(contribution.score.creativity)
        grouped[contribution.player_id]["technical_coherence"].append(contribution.score.technical_coherence)
        grouped[contribution.player_id]["inclusivity_awareness"].append(contribution.score.inclusivity_awareness)
        grouped[contribution.player_id]["collaboration"].append(contribution.score.collaboration)

    result: dict[str, dict[str, float]] = {}
    for player_id, dimension_values in grouped.items():
        result[player_id] = {
            dimension: round(mean(values), 2) if values else 0.0
            for dimension, values in dimension_values.items()
        }

    return result
