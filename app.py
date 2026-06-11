from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from components.styles import inject_styles, render_brand_header
from services.config import AppConfig
from services.multiplayer_service import get_room_store_status, state_from_record
from services.session_manager import GameSessionManager
from story_cube.collaborative_game import is_game_finished
from ui.game import render_game_screen
from ui.results import render_results_screen
from ui.setup import render_setup_screen

st.set_page_config(page_title="Story Cube I&D", page_icon="🎲", layout="wide")


def _sync_room_from_query(manager: GameSessionManager) -> None:
    try:
        query_room = str(st.query_params.get("room", "") or "").strip().upper()
    except Exception:
        query_room = ""

    if query_room and not manager.room_code:
        manager.room_code = query_room


def _resolve_screen(manager: GameSessionManager) -> str:
    if manager.game_state is None:
        return "setup"
    if is_game_finished(manager.game_state):
        return "results"
    return "game"


def render_screen(manager: GameSessionManager, config: AppConfig) -> None:
    room_store = None
    room_error = None

    if manager.play_mode == "supabase":
        room_store, room_error = get_room_store_status()

    screen_map = {
        "setup": lambda: render_setup_screen(manager, config, room_store, room_error, state_from_record),
        "game": lambda: render_game_screen(manager, config, room_store, state_from_record),
        "results": lambda: render_results_screen(PROJECT_ROOT, manager.game_state),
    }

    screen_map[_resolve_screen(manager)]()


def main() -> None:
    config = AppConfig()
    manager = GameSessionManager.from_streamlit()
    manager.init_defaults(config)

    inject_styles()
    _sync_room_from_query(manager)

    st.radio(
        "Play mode",
        options=["local", "supabase"],
        format_func=lambda mode: "Local single-screen" if mode == "local" else "Multiplayer shared room (Supabase)",
        key="play_mode",
        horizontal=True,
    )

    render_brand_header()
    render_screen(manager, config)


if __name__ == "__main__":
    main()
