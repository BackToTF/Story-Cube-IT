from __future__ import annotations

from pathlib import Path

import streamlit as st

from components.results_panel import render_final_results_cards
from services.game_service import export_session_artifacts
from story_cube.models import CollaborativeGameState


def render_results_screen(project_root: Path, state: CollaborativeGameState) -> None:
    st.markdown("<h2 class='screen-subtitle'>Final Results</h2>", unsafe_allow_html=True)

    if not render_final_results_cards(state):
        st.stop()

    json_path, xlsx_path = export_session_artifacts(project_root, state)
    st.caption(f"Session exported to {json_path.name} and {xlsx_path.name}.")
