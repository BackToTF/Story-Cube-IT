from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from story_cube.cube_data import CUBE_PACKS, DEFAULT_PACK
from story_cube.engine import assess_learning_signals, roll_default_cubes
from story_cube.exporter import export_session
from story_cube.game_modes import AVAILABLE_MODES
from story_cube.models import GameSession

st.set_page_config(page_title="Story Cube IT", page_icon="🎲", layout="wide")

st.title("Story Cube IT - Inclusion and Diversity")
st.caption("Learning by playing: data pipeline thinking, inclusion, and collaboration.")

pack_labels = {
    "data_pipeline_id": "Data Pipeline + I&D (ADF, Databricks, Governance)",
    "it_general": "General IT Creativity",
}

pack_name = st.selectbox(
    "Choose cube pack",
    options=list(CUBE_PACKS.keys()),
    index=list(CUBE_PACKS.keys()).index(DEFAULT_PACK),
    format_func=lambda key: pack_labels.get(key, key),
)

mode = st.selectbox(
    "Choose game mode",
    options=list(AVAILABLE_MODES.keys()),
    format_func=lambda key: f"{key} - {AVAILABLE_MODES[key]}",
)
players = st.slider("Number of players", min_value=1, max_value=10, value=3)
round_objective = st.text_input(
    "Mandatory round objective (message-first)",
    value="Include one perspective that is usually underrepresented in data decisions.",
)

if st.button("Roll cubes", type="primary"):
    st.session_state["rolled_faces"] = roll_default_cubes(pack_name=pack_name)
    st.session_state["active_pack_name"] = pack_name

rolled_faces = st.session_state.get("rolled_faces", [])
active_pack_name = st.session_state.get("active_pack_name")
if active_pack_name and active_pack_name != pack_name:
    st.info("Pack changed. Roll cubes again to align faces with the selected pack.")

if rolled_faces:
    st.subheader("Rolled faces")
    cols = st.columns(len(rolled_faces))
    for idx, face in enumerate(rolled_faces):
        with cols[idx]:
            st.metric(label=f"{face.cube_id} / face {face.face_id}", value=face.label)
            asset_name = f"die_{face.cube_id.lower()}_face_{face.label.lower().replace(' ', '_')}.svg"
            asset_path = PROJECT_ROOT / "assets" / "dice" / asset_name
            if asset_path.exists():
                st.image(str(asset_path), caption="Dice face")
            st.write(face.prompt)

story_text = st.text_area(
    "Write your pipeline story (orchestration -> ingestion -> transformation -> impact)",
    height=180,
)

if st.button("Assess signals and save session"):
    if not rolled_faces:
        st.error("Roll cubes before assessing session signals.")
    else:
        learning_signals = assess_learning_signals(story_text=story_text, rolled_faces=rolled_faces)
        score = learning_signals["signal_index"]

        st.subheader("Session signals (non-competitive)")
        st.caption("Use these as reflection aids for the team, not as ranking metrics.")
        signal_cols = st.columns(4)
        signal_cols[0].metric("Pipeline coverage", learning_signals["pipeline_coverage"])
        signal_cols[1].metric("Inclusion lens", learning_signals["inclusion_lens"])
        signal_cols[2].metric("Face alignment", learning_signals["face_alignment"])
        signal_cols[3].metric("Reflection depth", learning_signals["reflection_depth"])

        session = GameSession(
            mode=mode,
            players=players,
            rolled_faces=rolled_faces,
            story_text=f"Objective: {round_objective}\n\nStory: {story_text}",
            score=score,
        )
        json_path, xlsx_path = export_session(session, learning_signals=learning_signals)
        st.success(f"Session saved. Team signal index: {score}")
        st.write(f"JSON: {json_path}")
        st.write(f"XLSX: {xlsx_path}")
