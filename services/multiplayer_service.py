from __future__ import annotations

import os
from datetime import datetime

import streamlit as st

from services.config import AppConfig
from story_cube.models import CollaborativeGameState, ContributionScore, CubeFace, Player, StoryContribution
from story_cube.multiplayer_store import SUPABASE_IMPORT_ERROR, SupabaseRoomStore


def parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.utcnow()
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


@st.cache_resource(show_spinner=False)
def build_room_store(url: str, anon_key: str) -> SupabaseRoomStore:
    return SupabaseRoomStore(url=url, anon_key=anon_key)


def get_room_store_status() -> tuple[SupabaseRoomStore | None, str | None]:
    if SUPABASE_IMPORT_ERROR:
        return None, f"Supabase client import failed: {SUPABASE_IMPORT_ERROR}"

    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    anon_key = st.secrets.get("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not url or not anon_key:
        return None, "Set SUPABASE_URL and SUPABASE_ANON_KEY in Streamlit secrets or environment variables."

    try:
        return build_room_store(url, anon_key), None
    except Exception as exc:  # pragma: no cover
        return None, f"Supabase connection error: {exc}"


def state_from_record(record: dict, config: AppConfig) -> CollaborativeGameState:
    players = [
        Player(player_id=str(player["player_id"]), display_name=str(player["display_name"]))
        for player in record.get("players", [])
    ]

    contributions: list[StoryContribution] = []
    for item in record.get("contributions", []):
        faces = [
            CubeFace(
                cube_id=str(face["cube_id"]),
                face_id=int(face["face_id"]),
                label=str(face["label"]),
                prompt=str(face["prompt"]),
            )
            for face in item.get("rolled_faces", [])
        ]

        score_payload = item.get("score")
        score = None
        if score_payload:
            score = ContributionScore(
                creativity=float(score_payload.get("creativity", 0.0)),
                technical_coherence=float(score_payload.get("technical_coherence", 0.0)),
                inclusivity_awareness=float(score_payload.get("inclusivity_awareness", 0.0)),
                collaboration=float(score_payload.get("collaboration", 0.0)),
                clarity_coherence=float(score_payload.get("clarity_coherence", 0.0)),
            )

        contributions.append(
            StoryContribution(
                contribution_id=str(item["contribution_id"]),
                player_id=str(item["player_id"]),
                turn_index=int(item["turn_index"]),
                round_index=int(item["round_index"]),
                created_at=parse_datetime(item.get("created_at")),
                story_phase=str(item.get("story_phase", "once_upon_a_time")),
                rolled_faces=faces,
                text=str(item.get("text", "")),
                referenced_player_ids=[str(pid) for pid in item.get("referenced_player_ids", [])],
                included_quiet_player=bool(item.get("included_quiet_player", False)),
                selected_options=[str(option) for option in item.get("selected_options", [])],
                custom_text=str(item.get("custom_text", "")),
                is_intervention=bool(item.get("is_intervention", False)),
                intervening_player_id=item.get("intervening_player_id"),
                score=score,
                reviewer_archetype_hint=item.get("reviewer_archetype_hint"),
            )
        )

    return CollaborativeGameState(
        game_id=str(record.get("game_id", "")),
        mode=str(record.get("mode", config.default_mode)),
        game_mode=str(record.get("game_mode", "basic")),
        objective=str(record.get("objective", config.default_objective)),
        pack_name=str(record.get("pack_name", config.default_pack)),
        players=players,
        max_rounds=int(record.get("max_rounds", 3)),
        story_phase=str(record.get("story_phase", "once_upon_a_time")),
        current_round=int(record.get("current_round", 1)),
        current_turn=int(record.get("current_turn", 1)),
        contributions=contributions,
        created_at=parse_datetime(record.get("created_at")),
    )
