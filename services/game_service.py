from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from story_cube.collaborative_game import generate_profiles
from story_cube.collaborative_game import can_intervene, compose_story_text, current_player, submit_contribution
from story_cube.models import CollaborativeGameState
from story_cube.reviewer_agent import review_open_story


def get_player_name_map(state: CollaborativeGameState) -> dict[str, str]:
    return {player.player_id: player.display_name for player in state.players}


def generate_contribution_dataframe(state: CollaborativeGameState) -> pd.DataFrame:
    name_map = get_player_name_map(state)
    rows: list[dict[str, object]] = []
    for contribution in state.contributions:
        contributor_id = contribution.intervening_player_id or contribution.player_id
        rows.append(
            {
                "round": contribution.round_index,
                "turn": contribution.turn_index,
                "player": name_map.get(contributor_id, contributor_id),
                "text": contribution.text,
                "references": ", ".join(name_map.get(pid, pid) for pid in contribution.referenced_player_ids),
                "reviewer_hint": contribution.reviewer_archetype_hint,
                "creativity": contribution.score.creativity if contribution.score else None,
                "technical": contribution.score.technical_coherence if contribution.score else None,
                "inclusion": contribution.score.inclusivity_awareness if contribution.score else None,
                "collaboration": contribution.score.collaboration if contribution.score else None,
                "clarity": contribution.score.clarity_coherence if contribution.score else None,
                "total": contribution.score.total if contribution.score else None,
                "is_intervention": contribution.is_intervention,
                "story_phase": contribution.story_phase,
            }
        )
    return pd.DataFrame(rows)


def generate_profile_dataframe(state: CollaborativeGameState) -> pd.DataFrame:
    name_map = get_player_name_map(state)
    profiles = generate_profiles(state)
    participant_ids = {
        contribution.intervening_player_id or contribution.player_id
        for contribution in state.contributions
    }

    if not participant_ids:
        return pd.DataFrame(columns=["player", "archetype", "description", "contribution_style", "team_impact", "email_summary", "creativity", "technical", "inclusion", "collaboration", "clarity"])

    rows: list[dict[str, object]] = []
    for profile in profiles:
        if profile.player_id not in participant_ids:
            continue
        rows.append(
            {
                "player": name_map.get(profile.player_id, profile.player_id),
                "archetype": profile.dominant_archetype,
                "description": profile.description,
                "contribution_style": profile.contribution_style,
                "team_impact": profile.team_impact,
                "email_summary": profile.email_summary,
                "creativity": profile.dimension_averages.get("creativity", 0.0),
                "technical": profile.dimension_averages.get("technical_coherence", 0.0),
                "inclusion": profile.dimension_averages.get("inclusivity_awareness", 0.0),
                "collaboration": profile.dimension_averages.get("collaboration", 0.0),
                "clarity": profile.dimension_averages.get("clarity_coherence", 0.0),
            }
        )
    return pd.DataFrame(rows)


def build_email_ready_profiles(state: CollaborativeGameState) -> list[dict[str, object]]:
    name_map = get_player_name_map(state)
    rows: list[dict[str, object]] = []
    for profile in generate_profiles(state):
        rows.append(
            {
                "player": name_map.get(profile.player_id, profile.player_id),
                "archetype": profile.dominant_archetype,
                "explanation": profile.description,
                "contribution_style": profile.contribution_style,
                "team_impact": profile.team_impact,
                "email_summary": profile.email_summary,
                "dimensions": profile.dimension_averages,
            }
        )
    return rows


def export_session_artifacts(project_root: Path, state: CollaborativeGameState) -> tuple[Path, Path]:
    output_dir = project_root / "data" / "sessions" / "collaborative"
    output_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"game_{stamp}.json"
    xlsx_path = output_dir / f"game_{stamp}.xlsx"

    game_record = state.to_record()
    profiles_df = generate_profile_dataframe(state)
    game_record["profiles"] = profiles_df.to_dict(orient="records")

    with json_path.open("w", encoding="utf-8") as fp:
        json.dump(game_record, fp, indent=2)

    timeline_df = generate_contribution_dataframe(state)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        timeline_df.to_excel(writer, sheet_name="timeline", index=False)
        profiles_df.to_excel(writer, sheet_name="profiles", index=False)

    return json_path, xlsx_path


def evaluate_contribution(
    text: str,
    rolled_face_labels: list[str],
    referenced_player_ids: list[str],
    included_quiet_player: bool,
    story_phase: str | None = None,
    selected_options: list[str] | None = None,
    is_intervention: bool = False,
    intervening_player_id: str | None = None,
):
    return review_open_story(
        text=text,
        rolled_face_labels=rolled_face_labels,
        referenced_player_ids=referenced_player_ids,
        included_quiet_player=included_quiet_player,
        story_phase=story_phase,
        selected_options=selected_options,
        is_intervention=is_intervention,
        intervening_player_id=intervening_player_id,
    )
