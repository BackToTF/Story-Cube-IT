from __future__ import annotations

import streamlit as st

from services.config import AppConfig
from services.session_manager import GameSessionManager
from story_cube.collaborative_game import create_game


def _render_local_setup(manager: GameSessionManager, config: AppConfig) -> None:
    if manager.state["setup_step"] == "count":
        st.markdown("<h2 class='screen-subtitle'>Select number of players</h2>", unsafe_allow_html=True)
        with st.form("step_count_form"):
            player_count = st.slider("Players", min_value=2, max_value=12, value=int(manager.state["setup_player_count"]))
            next_step = st.form_submit_button("Next")

        if next_step:
            manager.state["setup_player_count"] = int(player_count)
            manager.state["setup_player_names"] = [f"Player {idx + 1}" for idx in range(int(player_count))]
            manager.state["setup_step"] = "names"
            st.rerun()
        st.stop()

    if manager.state["setup_step"] == "names":
        st.markdown("<h2 class='screen-subtitle'>Enter nicknames for the players</h2>", unsafe_allow_html=True)

        with st.form("step_names_form"):
            collected_names: list[str] = []
            for idx in range(manager.state["setup_player_count"]):
                default_name = manager.state["setup_player_names"][idx]
                name = st.text_input(f"Player {idx + 1}", value=default_name, key=f"player_name_{idx}")
                collected_names.append(name.strip())

            c_back, c_next = st.columns(2)
            go_back = c_back.form_submit_button("Back")
            go_next = c_next.form_submit_button("Next")

        if go_back:
            manager.state["setup_step"] = "count"
            st.rerun()
        if go_next:
            if any(not player_name for player_name in collected_names):
                st.error("Every player needs a name.")
            else:
                manager.state["setup_player_names"] = collected_names
                manager.state["setup_step"] = "start"
                st.rerun()
        st.stop()

    st.markdown("<h2 class='screen-subtitle'>Start the adventure</h2>", unsafe_allow_html=True)
    with st.form("step_start_form"):
        objective = st.text_input("Quest objective", value=manager.state["setup_objective"])
        rounds = st.slider("Rounds", min_value=1, max_value=5, value=int(manager.state["setup_rounds"]))
        game_mode = st.radio(
            "Story mode",
            options=["basic", "advanced"],
            format_func=lambda value: "Basic mode" if value == "basic" else "Advanced mode",
            index=0 if manager.state.get("setup_story_mode", config.default_story_mode) == "basic" else 1,
            horizontal=True,
        )
        c_back, c_start = st.columns(2)
        back_to_names = c_back.form_submit_button("Back")
        begin = c_start.form_submit_button("Start game")

    if back_to_names:
        manager.state["setup_step"] = "names"
        st.rerun()

    if begin:
        manager.state["setup_objective"] = objective
        manager.state["setup_rounds"] = int(rounds)
        manager.state["setup_story_mode"] = game_mode
        manager.game_state = create_game(
            player_names=manager.state["setup_player_names"],
            objective=objective,
            mode=config.default_mode,
            pack_name=config.default_pack,
            max_rounds=int(rounds),
            game_mode=game_mode,
        )
        manager.current_faces = []
        st.rerun()
    st.stop()


def _render_multiplayer_setup(manager: GameSessionManager, room_store, room_error: str | None, config: AppConfig, state_from_record_fn) -> None:
    if not room_store:
        st.error(room_error or "Supabase is not configured.")
        st.info("Add SUPABASE_URL and SUPABASE_ANON_KEY, then refresh the page.")
        st.stop()

    if not manager.room_code:
        st.markdown("<h2 class='screen-subtitle'>Create or join a shared room</h2>", unsafe_allow_html=True)
        tab_create, tab_join = st.tabs(["Create room", "Join room"])

        with tab_create:
            with st.form("create_room_form"):
                host_name = st.text_input("Your nickname", value=manager.player_name or "Host")
                expected_players = st.slider("Expected players", min_value=2, max_value=12, value=4)
                objective = st.text_input("Quest objective", value=manager.state["setup_objective"])
                rounds = st.slider("Rounds", min_value=1, max_value=5, value=int(manager.state["setup_rounds"]))
                game_mode = st.radio(
                    "Story mode",
                    options=["basic", "advanced"],
                    format_func=lambda value: "Basic mode" if value == "basic" else "Advanced mode",
                    index=0 if manager.state.get("setup_story_mode", config.default_story_mode) == "basic" else 1,
                    horizontal=True,
                )
                create_room = st.form_submit_button("Create and share room")

            if create_room:
                try:
                    room = room_store.create_room(
                        host_name=host_name,
                        expected_players=int(expected_players),
                        objective=objective,
                        max_rounds=int(rounds),
                        mode=config.default_mode,
                        pack_name=config.default_pack,
                        game_mode=game_mode,
                    )
                    manager.room_code = str(room["room_code"])
                    manager.player_name = host_name
                    manager.state["setup_objective"] = objective
                    manager.state["setup_rounds"] = int(rounds)
                    manager.state["setup_story_mode"] = game_mode
                    st.rerun()
                except Exception as exc:
                    st.error(f"Room creation failed: {exc}")

        with tab_join:
            with st.form("join_room_form"):
                join_code = st.text_input("Room code", value=manager.room_code).strip().upper()
                join_name = st.text_input("Your nickname", value=manager.player_name)
                join_room = st.form_submit_button("Join room")

            if join_room:
                try:
                    room_store.join_room(room_code=join_code, player_name=join_name)
                    manager.room_code = join_code
                    manager.player_name = join_name
                    st.rerun()
                except Exception as exc:
                    st.error(f"Join failed: {exc}")

        st.stop()

    room_code = manager.room_code
    room = room_store.get_room(room_code)

    if not room:
        st.error("Room not found. It may have been deleted.")
        if st.button("Clear room and return"):
            manager.room_code = ""
            manager.game_state = None
            st.rerun()
        st.stop()

    try:
        st.query_params["room"] = room_code
    except Exception:
        pass

    players = [str(player.get("display_name", "")).strip() for player in room.get("players") or []]
    players = [name for name in players if name]
    player_name = manager.player_name

    st.caption(f"Room code: {room_code} | share URL with ?room={room_code}")
    st.write("Players in room: " + (", ".join(players) if players else "none"))

    if room.get("status") == "lobby":
        host_name = str(room.get("host_name", "")).strip()
        is_host = bool(player_name) and player_name == host_name
        needed = max(2, int(room.get("expected_players") or 2))
        st.info(f"Lobby mode. Host: {host_name or 'n/a'}. Players joined: {len(players)}/{needed}.")

        if is_host:
            can_start = len(players) >= 2
            if st.button("Start multiplayer game", disabled=not can_start, type="primary"):
                state = create_game(
                    player_names=players,
                    objective=str(room.get("objective") or config.default_objective),
                    mode=str(room.get("mode") or config.default_mode),
                    pack_name=str(room.get("pack_name") or config.default_pack),
                    max_rounds=int(room.get("max_rounds") or 3),
                    game_mode=str(room.get("game_mode") or manager.state.get("setup_story_mode", config.default_story_mode)),
                )
                room_store.update_room(room_code, {"status": "active", "game_state": state.to_record()})
                manager.current_faces = []
                st.rerun()
        else:
            st.warning("Waiting for host to start the match.")
            if st.button("Refresh room"):
                st.rerun()

        st.stop()

    game_payload = room.get("game_state")
    if not game_payload:
        st.error("Game state missing in room. Ask host to restart the room.")
        st.stop()

    manager.game_state = state_from_record_fn(game_payload, config)


def render_setup_screen(manager: GameSessionManager, config: AppConfig, room_store, room_error: str | None, state_from_record_fn) -> None:
    if manager.play_mode == "supabase":
        _render_multiplayer_setup(manager, room_store, room_error, config, state_from_record_fn)
    else:
        _render_local_setup(manager, config)
