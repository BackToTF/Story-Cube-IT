from __future__ import annotations

import html

import streamlit as st

from services.game_service import generate_profile_dataframe, get_player_name_map
from services.game_service import build_email_ready_profiles
from story_cube.collaborative_game import generate_profiles
from story_cube.models import CollaborativeGameState


def render_player_profile_panel(state: CollaborativeGameState, player_name: str) -> None:
    profiles = generate_profiles(state)
    name_map = get_player_name_map(state)
    reverse_map = {v: k for k, v in name_map.items()}
    player_id = reverse_map.get(player_name)
    profile = next((p for p in profiles if p.player_id == player_id), None)

    archetype = "In Progress"
    description = "Play your turns to unlock your archetype profile."

    if profile and any((contribution.intervening_player_id or contribution.player_id) == player_id for contribution in state.contributions):
        archetype = profile.dominant_archetype
        description = profile.description

    st.markdown(
        f"""
        <div class='results-side'>
          <h4 class='results-side-title'>Your Results</h4>
          <div style='font-size:3rem;'>🎯</div>
          <div class='results-side-archetype'>{html.escape(archetype)}</div>
          <div class='results-side-text'>{html.escape(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_final_results_cards(state: CollaborativeGameState) -> bool:
    profiles_df = generate_profile_dataframe(state)
    if profiles_df.empty:
        st.info("No completed contributions found yet.")
        return False

    email_ready_profiles = build_email_ready_profiles(state)

    for row in profiles_df.to_dict(orient="records"):
        player = html.escape(str(row["player"]))
        archetype = html.escape(str(row["archetype"]))
        description = html.escape(str(row["description"]))
        icon = player[:1].upper() if player else "P"
        extra = next((item for item in email_ready_profiles if item["player"] == row["player"]), None)
        email_summary = html.escape(str(extra["email_summary"])) if extra else description
        st.markdown(
            f"""
            <div class='final-card'>
              <div class='final-player'>{player}</div>
              <div class='final-row'>
                <div class='final-icon'>{icon}</div>
                <div>
                  <p class='final-archetype'>{archetype}</p>
                  <div class='final-description'>{description}</div>
                  <div class='final-email'>{email_summary}</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return True
