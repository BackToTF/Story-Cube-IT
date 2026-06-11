from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from .archetypes import build_player_profile
from .engine import roll_cube_faces, roll_default_cubes
from .models import (
    STORY_PHASE_SEQUENCE,
    CollaborativeGameState,
    ContributionScore,
    Player,
    PlayerProfile,
    StoryContribution,
)
from .scoring import aggregate_player_dimension_averages, score_contribution


def _phase_for_turn(turn_index: int) -> str:
    return STORY_PHASE_SEQUENCE[(max(1, turn_index) - 1) % len(STORY_PHASE_SEQUENCE)]


PHASE_CUBE_MAP = {
    "once_upon_a_time": "OnceUpon",
    "who": "Character",
    "where": "Setting",
    "what": "Event",
    "problem": "Problem",
    "resolution": "Resolution",
}


def compose_story_text(selected_options: list[str] | None = None, custom_text: str = "") -> str:
    selected_options = [option.strip() for option in (selected_options or []) if option.strip()]
    custom_text = custom_text.strip()
    pieces = selected_options[:]
    if custom_text:
        pieces.append(custom_text)
    return " | ".join(pieces)


def roll_phase_face(state: CollaborativeGameState, seed: int | None = None):
    cube_name = PHASE_CUBE_MAP.get(state.story_phase, "Event")
    try:
        return roll_cube_faces(cube_name, count=1, seed=seed, pack_name=state.pack_name)[0]
    except ValueError:
        return roll_default_cubes(seed=seed, pack_name=state.pack_name)[0]


def create_game(
    player_names: list[str],
    objective: str,
    mode: str = "pipeline_story",
    pack_name: str = "data_pipeline_id",
    max_rounds: int = 3,
    game_mode: str = "basic",
) -> CollaborativeGameState:
    players = [
        Player(player_id=f"P{idx + 1}", display_name=name)
        for idx, name in enumerate(player_names)
    ]
    return CollaborativeGameState(
        game_id=str(uuid4()),
        mode=mode,
        objective=objective,
        pack_name=pack_name,
        game_mode=game_mode,
        players=players,
        max_rounds=max_rounds,
        story_phase=STORY_PHASE_SEQUENCE[0],
    )


def current_player(state: CollaborativeGameState) -> Player:
    index = (state.current_turn - 1) % len(state.players)
    return state.players[index]


def roll_turn_faces(state: CollaborativeGameState, seed: int | None = None):
    return roll_phase_face(state, seed=seed)


def player_intervention_count(state: CollaborativeGameState, player_id: str, round_index: int | None = None) -> int:
    return sum(
        1
        for contribution in state.contributions
        if contribution.is_intervention
        and contribution.intervening_player_id == player_id
        and (round_index is None or contribution.round_index == round_index)
    )


def can_intervene(state: CollaborativeGameState, player_id: str) -> bool:
    if current_player(state).player_id == player_id:
        return False
    return player_intervention_count(state, player_id, state.current_round) < 1


def submit_contribution(
    state: CollaborativeGameState,
    text: str,
    rolled_faces,
    referenced_player_ids: list[str] | None = None,
    included_quiet_player: bool = False,
    selected_options: list[str] | None = None,
    custom_text: str = "",
    story_phase: str | None = None,
    is_intervention: bool = False,
    intervening_player_id: str | None = None,
    manual_score: ContributionScore | None = None,
    reviewer_archetype_hint: str | None = None,
) -> StoryContribution:
    referenced_player_ids = referenced_player_ids or []
    selected_options = selected_options or []
    current_phase = story_phase or state.story_phase or _phase_for_turn(state.current_turn)
    narrative_text = text.strip() or compose_story_text(selected_options, custom_text)
    score = manual_score
    if not score:
        score = score_contribution(
            text=narrative_text,
            rolled_face_labels=[face.label for face in rolled_faces],
            referenced_player_ids=referenced_player_ids,
            included_quiet_player=included_quiet_player,
            story_phase=current_phase,
            selected_options=selected_options,
            is_intervention=is_intervention,
            intervening_player_id=intervening_player_id,
        )

    contribution = StoryContribution(
        contribution_id=str(uuid4()),
        player_id=current_player(state).player_id,
        turn_index=state.current_turn,
        round_index=state.current_round,
        created_at=datetime.utcnow(),
        story_phase=current_phase,
        rolled_faces=rolled_faces,
        text=narrative_text,
        referenced_player_ids=referenced_player_ids,
        included_quiet_player=included_quiet_player,
        selected_options=selected_options,
        custom_text=custom_text.strip(),
        is_intervention=is_intervention,
        intervening_player_id=intervening_player_id,
        score=score,
        reviewer_archetype_hint=reviewer_archetype_hint,
    )

    state.contributions.append(contribution)
    if not is_intervention:
        state.current_turn += 1
        if ((state.current_turn - 1) % len(state.players)) == 0:
            state.current_round += 1
        state.story_phase = _phase_for_turn(state.current_turn)
    else:
        state.story_phase = current_phase

    return contribution


def is_game_finished(state: CollaborativeGameState) -> bool:
    return state.current_round > state.max_rounds


def generate_profiles(state: CollaborativeGameState) -> list[PlayerProfile]:
    averages = aggregate_player_dimension_averages(state.contributions)
    profiles: list[PlayerProfile] = []
    for player in state.players:
        player_avg = averages.get(
            player.player_id,
            {
                "creativity": 0.0,
                "technical_coherence": 0.0,
                "inclusivity_awareness": 0.0,
                "collaboration": 0.0,
                "clarity_coherence": 0.0,
            },
        )
        profiles.append(build_player_profile(player.player_id, player_avg))
    return profiles
