from __future__ import annotations

from .models import PlayerProfile


ARCHETYPE_DEFINITIONS = {
    "Logical": "Strong in technical structure and coherent data pipeline reasoning.",
    "Creative": "Generates vivid and imaginative narrative moves.",
    "Connector": "Builds bridges across teammates ideas and keeps the story cohesive.",
    "Innovator": "Proposes unconventional but useful approaches.",
    "Facilitator": "Maintains group flow and supports balanced participation.",
    "Analytical": "Highlights detail, quality checks, and consistency.",
    "Empathetic": "Prioritizes inclusion, diverse perspectives, and human impact.",
}


def map_dimensions_to_archetype(dimension_averages: dict[str, float]) -> str:
    creativity = dimension_averages.get("creativity", 0.0)
    technical = dimension_averages.get("technical_coherence", 0.0)
    inclusivity = dimension_averages.get("inclusivity_awareness", 0.0)
    collaboration = dimension_averages.get("collaboration", 0.0)

    if inclusivity >= 4.0 and collaboration >= 3.8:
        return "Empathetic"
    if collaboration >= 4.1:
        return "Connector"
    if technical >= 4.2 and inclusivity >= 3.2:
        return "Logical"
    if technical >= 4.3:
        return "Analytical"
    if creativity >= 4.3 and technical >= 3.0:
        return "Innovator"
    if creativity >= 4.1:
        return "Creative"
    return "Facilitator"


def build_player_profile(player_id: str, dimension_averages: dict[str, float]) -> PlayerProfile:
    archetype = map_dimensions_to_archetype(dimension_averages)
    return PlayerProfile(
        player_id=player_id,
        dominant_archetype=archetype,
        description=ARCHETYPE_DEFINITIONS[archetype],
        dimension_averages=dimension_averages,
    )
