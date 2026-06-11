from __future__ import annotations

from .models import PlayerProfile


ARCHETYPE_DEFINITIONS = {
    "Logical": {
        "description": "Strong in technical structure and coherent data pipeline reasoning.",
        "style": "Structured, precise, and systems-oriented.",
        "impact": "Turns ambiguity into a clean sequence the team can follow.",
    },
    "Creative": {
        "description": "Generates vivid and imaginative narrative moves.",
        "style": "Inventive, surprising, and idea-rich.",
        "impact": "Keeps the story fresh and prevents flat moments.",
    },
    "Connector": {
        "description": "Builds bridges across teammates ideas and keeps the story cohesive.",
        "style": "Bridging, relational, and continuity-focused.",
        "impact": "Links contributions together so nobody feels dropped.",
    },
    "Innovator": {
        "description": "Proposes unconventional but useful approaches.",
        "style": "Experimental, bold, and adaptive.",
        "impact": "Introduces new paths when the group gets stuck.",
    },
    "Facilitator": {
        "description": "Maintains group flow and supports balanced participation.",
        "style": "Guiding, balanced, and participation-aware.",
        "impact": "Keeps the room moving and lowers participation friction.",
    },
    "Analytical": {
        "description": "Highlights detail, quality checks, and consistency.",
        "style": "Careful, validating, and coherence-driven.",
        "impact": "Reduces errors and strengthens the story logic.",
    },
    "Empathetic": {
        "description": "Prioritizes inclusion, diverse perspectives, and human impact.",
        "style": "Inclusive, considerate, and human-centered.",
        "impact": "Makes space for quieter voices and wider perspectives.",
    },
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
    definition = ARCHETYPE_DEFINITIONS[archetype]
    return PlayerProfile(
        player_id=player_id,
        dominant_archetype=archetype,
        description=definition["description"],
        dimension_averages=dimension_averages,
        contribution_style=definition["style"],
        team_impact=definition["impact"],
        email_summary=f"{archetype}: {definition['description']} Team impact: {definition['impact']}",
    )
