from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .models import ContributionScore
from .scoring import score_contribution


@dataclass(frozen=True)
class AgentReview:
    score: ContributionScore
    archetype_hint: str
    rationale: str


def _archetype_from_score(score: ContributionScore) -> str:
    if score.inclusivity_awareness >= 4.2 and score.collaboration >= 4.0:
        return "Empathetic"
    if score.collaboration >= 4.2:
        return "Connector"
    if score.technical_coherence >= 4.3:
        return "Analytical"
    if score.creativity >= 4.4 and score.technical_coherence >= 3.2:
        return "Innovator"
    if score.creativity >= 4.2:
        return "Creative"
    if score.technical_coherence >= 4.0:
        return "Logical"
    return "Facilitator"


def review_open_story(
    text: str,
    rolled_face_labels: list[str],
    referenced_player_ids: list[str] | None = None,
    included_quiet_player: bool = False,
    story_phase: str | None = None,
    selected_options: list[str] | None = None,
    is_intervention: bool = False,
    intervening_player_id: str | None = None,
) -> AgentReview:
    score = score_contribution(
        text=text,
        rolled_face_labels=rolled_face_labels,
        referenced_player_ids=referenced_player_ids,
        included_quiet_player=included_quiet_player,
        story_phase=story_phase,
        selected_options=selected_options,
        is_intervention=is_intervention,
        intervening_player_id=intervening_player_id,
    )
    archetype_hint = _archetype_from_score(score)
    rationale = (
        "Auto-review agent evaluated creativity, technical coherence, inclusion lens, and collaboration signals "
        "from your story block."
    )
    return AgentReview(score=score, archetype_hint=archetype_hint, rationale=rationale)


def review_multiple_choice(option_payloads: list[dict[str, object]]) -> AgentReview:
    if not option_payloads:
        base = ContributionScore(2.0, 2.0, 2.0, 2.0, 2.0)
        return AgentReview(base, "Facilitator", "No options selected, default neutral profile applied.")

    creativity = 0.0
    technical = 0.0
    inclusivity = 0.0
    collaboration = 0.0
    archetypes: list[str] = []

    for payload in option_payloads:
        score = payload.get("score", {})
        creativity += float(score.get("creativity", 0.0))
        technical += float(score.get("technical_coherence", 0.0))
        inclusivity += float(score.get("inclusivity_awareness", 0.0))
        collaboration += float(score.get("collaboration", 0.0))
        archetypes.append(str(payload.get("archetype", "Facilitator")))

    n = float(len(option_payloads))
    contribution_score = ContributionScore(
        creativity=round(creativity / n, 2),
        technical_coherence=round(technical / n, 2),
        inclusivity_awareness=round(inclusivity / n, 2),
        collaboration=round(collaboration / n, 2),
        clarity_coherence=2.0,
    )

    archetype_hint = Counter(archetypes).most_common(1)[0][0]
    rationale = "Auto-review agent mapped selected options to archetype vectors and aggregated the score."
    return AgentReview(contribution_score, archetype_hint, rationale)
