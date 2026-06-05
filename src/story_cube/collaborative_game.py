from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from .archetypes import build_player_profile
from .engine import roll_default_cubes
from .models import CollaborativeGameState, ContributionScore, Player, PlayerProfile, StoryContribution
from .scoring import aggregate_player_dimension_averages, score_contribution


def create_game(
    player_names: list[str],
    objective: str,
    mode: str = "pipeline_story",
    pack_name: str = "data_pipeline_id",
    max_rounds: int = 3,
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
        players=players,
        max_rounds=max_rounds,
    )


def current_player(state: CollaborativeGameState) -> Player:
    index = (state.current_turn - 1) % len(state.players)
    return state.players[index]


def roll_turn_faces(state: CollaborativeGameState, seed: int | None = None):
    return roll_default_cubes(seed=seed, pack_name=state.pack_name)[:3]


def submit_contribution(
    state: CollaborativeGameState,
    text: str,
    rolled_faces,
    referenced_player_ids: list[str] | None = None,
    included_quiet_player: bool = False,
    manual_score: ContributionScore | None = None,
    reviewer_archetype_hint: str | None = None,
) -> StoryContribution:
    referenced_player_ids = referenced_player_ids or []
    score = manual_score
    if not score:
        score = score_contribution(
            text=text,
            rolled_face_labels=[face.label for face in rolled_faces],
            referenced_player_ids=referenced_player_ids,
            included_quiet_player=included_quiet_player,
        )

    contribution = StoryContribution(
        contribution_id=str(uuid4()),
        player_id=current_player(state).player_id,
        turn_index=state.current_turn,
        round_index=state.current_round,
        created_at=datetime.utcnow(),
        rolled_faces=rolled_faces,
        text=text,
        referenced_player_ids=referenced_player_ids,
        included_quiet_player=included_quiet_player,
        score=score,
        reviewer_archetype_hint=reviewer_archetype_hint,
    )

    state.contributions.append(contribution)
    state.current_turn += 1
    if ((state.current_turn - 1) % len(state.players)) == 0:
        state.current_round += 1

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
            },
        )
        profiles.append(build_player_profile(player.player_id, player_avg))
    return profiles
