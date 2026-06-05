from __future__ import annotations

import html
import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from story_cube.collaborative_game import create_game, current_player, generate_profiles, is_game_finished, submit_contribution
from story_cube.cube_data import CUBE_PACKS, DEFAULT_PACK
from story_cube.models import CollaborativeGameState, ContributionScore, CubeFace, Player, StoryContribution
from story_cube.multiplayer_store import SUPABASE_IMPORT_ERROR, SupabaseRoomStore
from story_cube.reviewer_agent import review_open_story

st.set_page_config(page_title="Story Cube I&D", page_icon="*", layout="wide")

DEFAULT_MODE = "collaborative"
DEFAULT_OBJECTIVE = "Build a surreal IT adventure that still keeps a plausible data-stack backbone and inclusive impact."


def _parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.utcnow()
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


@st.cache_resource(show_spinner=False)
def _build_room_store(url: str, anon_key: str) -> SupabaseRoomStore:
    return SupabaseRoomStore(url=url, anon_key=anon_key)


def _multiplayer_store_status() -> tuple[SupabaseRoomStore | None, str | None]:
    if SUPABASE_IMPORT_ERROR:
        return None, f"Supabase client import failed: {SUPABASE_IMPORT_ERROR}"

    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    anon_key = st.secrets.get("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not url or not anon_key:
        return None, "Set SUPABASE_URL and SUPABASE_ANON_KEY in Streamlit secrets or environment variables."

    try:
        return _build_room_store(url, anon_key), None
    except Exception as exc:  # pragma: no cover
        return None, f"Supabase connection error: {exc}"


def _state_from_record(record: dict) -> CollaborativeGameState:
    players = [Player(player_id=str(p["player_id"]), display_name=str(p["display_name"])) for p in record.get("players", [])]

    contributions: list[StoryContribution] = []
    for item in record.get("contributions", []):
        faces = [
            CubeFace(cube_id=str(f["cube_id"]), face_id=int(f["face_id"]), label=str(f["label"]), prompt=str(f["prompt"]))
            for f in item.get("rolled_faces", [])
        ]

        score_payload = item.get("score")
        score = None
        if score_payload:
            score = ContributionScore(
                creativity=float(score_payload.get("creativity", 0.0)),
                technical_coherence=float(score_payload.get("technical_coherence", 0.0)),
                inclusivity_awareness=float(score_payload.get("inclusivity_awareness", 0.0)),
                collaboration=float(score_payload.get("collaboration", 0.0)),
            )

        contributions.append(
            StoryContribution(
                contribution_id=str(item["contribution_id"]),
                player_id=str(item["player_id"]),
                turn_index=int(item["turn_index"]),
                round_index=int(item["round_index"]),
                created_at=_parse_datetime(item.get("created_at")),
                rolled_faces=faces,
                text=str(item.get("text", "")),
                referenced_player_ids=[str(pid) for pid in item.get("referenced_player_ids", [])],
                included_quiet_player=bool(item.get("included_quiet_player", False)),
                score=score,
                reviewer_archetype_hint=item.get("reviewer_archetype_hint"),
            )
        )

    return CollaborativeGameState(
        game_id=str(record.get("game_id", "")),
        mode=str(record.get("mode", DEFAULT_MODE)),
        objective=str(record.get("objective", DEFAULT_OBJECTIVE)),
        pack_name=str(record.get("pack_name", DEFAULT_PACK)),
        players=players,
        max_rounds=int(record.get("max_rounds", 3)),
        current_round=int(record.get("current_round", 1)),
        current_turn=int(record.get("current_turn", 1)),
        contributions=contributions,
        created_at=_parse_datetime(record.get("created_at")),
    )


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800&family=Nunito+Sans:wght@400;600;700&display=swap');

        .stApp { font-family: 'Nunito Sans', sans-serif; background: radial-gradient(1300px 800px at 50% -20%, #ffffff 0%, #f7f7f4 62%, #f3f3f1 100%); }

        .main .block-container {
            max-width: 1120px;
            padding: 1.2rem 2rem 2.2rem 2rem;
            border: 1px solid #cfd7de;
            border-radius: 26px;
            background: #fbfbfa;
            box-shadow: 0 18px 42px rgba(15, 36, 56, 0.10);
            margin-top: 20px;
            margin-bottom: 36px;
        }

        .brand-wrap { text-align: center; margin: 8px 0 10px 0; }
        .brand-line { display: inline-flex; align-items: center; gap: 10px; }
        .brand-main {
            margin: 0;
            font-size: clamp(2.2rem, 5vw, 5.2rem);
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            letter-spacing: 0.03em;
            color: #003a63;
            line-height: 1;
            text-shadow: 0 1px 0 #001f35;
            text-transform: uppercase;
        }
        .brand-sub {
            margin-top: 6px;
            font-size: clamp(1.8rem, 4vw, 4rem);
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            letter-spacing: 0.04em;
            color: #ff9f00;
            text-shadow: 0 1px 0 #d27400;
            text-transform: uppercase;
        }
        .brand-dice {
            width: 46px; height: 46px; border: 3px solid #003a63; border-radius: 12px;
            display: inline-grid; grid-template-columns: repeat(3, 1fr); gap: 3px; padding: 6px;
            background: linear-gradient(180deg, #eff8ff 0%, #dcefff 100%); box-shadow: 0 3px 0 #001f35;
        }
        .brand-dice span {
            width: 8px; height: 8px; border-radius: 50%; background: #1a5b8d;
            justify-self: center; align-self: center; opacity: 0;
        }
        .brand-dice span:nth-child(1), .brand-dice span:nth-child(3), .brand-dice span:nth-child(5), .brand-dice span:nth-child(7), .brand-dice span:nth-child(9) { opacity: 1; }

        .screen-subtitle {
            text-align: center;
            font-size: clamp(1.7rem, 2.6vw, 2.5rem);
            color: #003a63;
            margin: 0;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            text-shadow: 0 1px 0 #001f35;
        }
        .screen-note { text-align: center; font-size: clamp(1.1rem, 1.8vw, 1.9rem); color: #10273d; margin: 2px 0 10px 0; }
        .section-title {
            margin: 10px 0 10px 0; padding-top: 6px; border-top: 3px solid #0f4c73;
            font-family: 'Montserrat', sans-serif; font-size: clamp(1.9rem, 2.8vw, 2.8rem);
            color: #003a63; letter-spacing: 0.02em; text-transform: uppercase; font-weight: 800;
        }

        .stButton button, .stFormSubmitButton button {
            border: 1px solid #d77a00; border-radius: 14px; font-weight: 800; font-family: 'Montserrat', sans-serif;
            font-size: 1.06rem; background: linear-gradient(180deg, #ffa600 0%, #ff9800 100%);
            color: #ffffff; text-shadow: 0 1px 0 #b55f00; box-shadow: 0 2px 0 #d77a00; min-height: 54px;
        }

        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            border: 2px solid #c3ced8 !important; border-radius: 14px !important; background: #ffffff !important;
            color: #112336 !important; font-size: 1.05rem !important;
        }

        .stSlider [role='slider'] { background: #ffb000 !important; box-shadow: 0 0 0 2px #ff9800 !important; }

        .dice-roll-stage { border-radius: 16px; border: 1px dashed #99afc1; padding: 10px; background: #ffffff; color: #003a63; text-align: center; font-weight: 700; }

        .dice-icon-card {
            border: 2px solid #0f4c73; border-radius: 22px; padding: 10px 8px; background: #fbfbfa;
            box-shadow: 0 6px 0 rgba(15, 76, 115, 0.18); margin: 0 auto; max-width: 210px;
        }
        .dice-mini-label { text-align: center; color: #0f4c73; font-weight: 800; margin-top: 8px; font-size: 0.96rem; }

        .story-row { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 10px; }
        .story-avatar {
            width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
            font-family: 'Montserrat', sans-serif; font-size: 1.2rem; font-weight: 800; color: #fff;
            border: 2px solid #d77a00; background: linear-gradient(180deg, #ffb000 0%, #ff8f00 100%); box-shadow: 0 2px 0 #d77a00;
        }
        .story-bubble { flex: 1; border: 2px solid #d4dce3; border-radius: 16px; background: #ffffff; padding: 12px 14px; }
        .story-name { font-family: 'Montserrat', sans-serif; color: #003a63; font-size: 1.05rem; margin-bottom: 4px; font-weight: 700; }
        .story-text { margin: 0; color: #102133; font-size: 1.02rem; line-height: 1.4; }

        .results-side { border: 2px solid #d4dce3; border-radius: 16px; background: #ffffff; padding: 14px; text-align: center; min-height: 280px; }
        .results-side-title { font-family: 'Montserrat', sans-serif; color: #003a63; font-size: 2rem; margin: 0 0 8px 0; text-transform: uppercase; font-weight: 800; }
        .results-side-archetype { color: #003a63; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 2.1rem; margin: 6px 0; }
        .results-side-text { color: #112336; font-size: 1.2rem; line-height: 1.35; }

        .final-card { border: 2px solid #c7d3de; border-radius: 18px; background: #fff; padding: 18px; margin-bottom: 14px; }
        .final-player { color: #003a63; font-family: 'Montserrat', sans-serif; font-size: 1.9rem; margin: 0 0 8px 0; font-weight: 800; }
        .final-row { display: flex; gap: 12px; align-items: center; }
        .final-icon {
            width: 64px; height: 64px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
            font-family: 'Montserrat', sans-serif; font-size: 1.7rem; font-weight: 800; color: #fff;
            border: 2px solid #d77a00; background: linear-gradient(180deg, #ffb000 0%, #ff8f00 100%); box-shadow: 0 2px 0 #d77a00;
        }
        .final-archetype { color: #003a63; font-family: 'Montserrat', sans-serif; font-size: 2.4rem; margin: 0; font-weight: 800; }
        .final-description { margin-top: 4px; color: #112336; font-size: 1.25rem; line-height: 1.35; }

        @media (max-width: 900px) {
            .main .block-container { padding: 1rem 1rem 1.8rem 1rem; border-radius: 18px; }
            .brand-dice { width: 40px; height: 40px; }
            .story-avatar, .final-icon { width: 44px; height: 44px; font-size: 1.2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_brand_header() -> None:
    st.markdown(
        """
        <div class='brand-wrap'>
          <div class='brand-line'>
            <div class='brand-dice'>
              <span></span><span></span><span></span>
              <span></span><span></span><span></span>
              <span></span><span></span><span></span>
            </div>
            <h1 class='brand-main'>STORY CUBE</h1>
          </div>
          <div class='brand-sub'>I&D EDITION</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _player_name_map(state: CollaborativeGameState) -> dict[str, str]:
    return {p.player_id: p.display_name for p in state.players}


def _contributions_dataframe(state: CollaborativeGameState) -> pd.DataFrame:
    name_map = _player_name_map(state)
    rows: list[dict[str, object]] = []
    for contribution in state.contributions:
        rows.append(
            {
                "round": contribution.round_index,
                "turn": contribution.turn_index,
                "player": name_map.get(contribution.player_id, contribution.player_id),
                "text": contribution.text,
                "references": ", ".join(name_map.get(pid, pid) for pid in contribution.referenced_player_ids),
                "reviewer_hint": contribution.reviewer_archetype_hint,
                "creativity": contribution.score.creativity if contribution.score else None,
                "technical": contribution.score.technical_coherence if contribution.score else None,
                "inclusion": contribution.score.inclusivity_awareness if contribution.score else None,
                "collaboration": contribution.score.collaboration if contribution.score else None,
                "total": contribution.score.total if contribution.score else None,
            }
        )
    return pd.DataFrame(rows)


def _profile_dataframe(state: CollaborativeGameState) -> pd.DataFrame:
    name_map = _player_name_map(state)
    profiles = generate_profiles(state)
    participant_ids = {contribution.player_id for contribution in state.contributions}

    if not participant_ids:
        return pd.DataFrame(columns=["player", "archetype", "description", "creativity", "technical", "inclusion", "collaboration"])

    rows: list[dict[str, object]] = []
    for profile in profiles:
        if profile.player_id not in participant_ids:
            continue
        rows.append(
            {
                "player": name_map.get(profile.player_id, profile.player_id),
                "archetype": profile.dominant_archetype,
                "description": profile.description,
                "creativity": profile.dimension_averages.get("creativity", 0.0),
                "technical": profile.dimension_averages.get("technical_coherence", 0.0),
                "inclusion": profile.dimension_averages.get("inclusivity_awareness", 0.0),
                "collaboration": profile.dimension_averages.get("collaboration", 0.0),
            }
        )
    return pd.DataFrame(rows)


def _save_collaborative_export(state: CollaborativeGameState) -> tuple[Path, Path]:
    output_dir = PROJECT_ROOT / "data" / "sessions" / "collaborative"
    output_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"game_{stamp}.json"
    xlsx_path = output_dir / f"game_{stamp}.xlsx"

    game_record = state.to_record()
    profiles_df = _profile_dataframe(state)
    game_record["profiles"] = profiles_df.to_dict(orient="records")

    with json_path.open("w", encoding="utf-8") as fp:
        json.dump(game_record, fp, indent=2)

    timeline_df = _contributions_dataframe(state)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        timeline_df.to_excel(writer, sheet_name="timeline", index=False)
        profiles_df.to_excel(writer, sheet_name="profiles", index=False)

    return json_path, xlsx_path


def _cube_palette(cube_id: str) -> tuple[str, str]:
    palette = {
        "Orchestration": ("#f97316", "#ea580c"),
        "Ingestion": ("#06b6d4", "#0e7490"),
        "Transformation": ("#3b82f6", "#1d4ed8"),
        "InclusionLens": ("#22c55e", "#15803d"),
        "AI": ("#0ea5e9", "#0284c7"),
        "Cloud": ("#38bdf8", "#0ea5e9"),
        "People": ("#f59e0b", "#f97316"),
    }
    return palette.get(cube_id, ("#64748b", "#334155"))


def _face_svg(face: CubeFace) -> str:
    c1, c2 = _cube_palette(face.cube_id)
    gradient_id = f"g_{face.cube_id}_{face.face_id}".replace("-", "_")
    label = face.label.replace("&", "and")

    return f"""
    <svg width='168' height='168' viewBox='0 0 168 168' xmlns='http://www.w3.org/2000/svg'>
      <defs>
        <linearGradient id='{gradient_id}' x1='0' y1='0' x2='1' y2='1'>
          <stop offset='0%' stop-color='{c1}'/>
          <stop offset='100%' stop-color='{c2}'/>
        </linearGradient>
      </defs>
      <polygon points='84,8 148,44 148,124 84,160 20,124 20,44' fill='url(#{gradient_id})' stroke='#0f4c73' stroke-width='4'/>
      <polygon points='84,24 134,52 134,116 84,144 34,116 34,52' fill='rgba(255,255,255,0.94)' stroke='#0f4c73' stroke-width='2.2'/>
      <text x='84' y='82' text-anchor='middle' font-family='Montserrat, sans-serif' font-size='16' font-weight='800' fill='#0f4c73'>{html.escape(label[:11])}</text>
      <text x='84' y='104' text-anchor='middle' font-family='Nunito Sans, sans-serif' font-size='11' font-weight='700' fill='#16486b'>d{face.face_id}</text>
    </svg>
    """


def _render_faces(rolled_faces: list[CubeFace]) -> None:
    row = st.columns(3)
    for idx, face in enumerate(rolled_faces[:3]):
        with row[idx]:
            svg_markup = _face_svg(face)
            svg_data_uri = f"data:image/svg+xml;utf8,{quote(svg_markup)}"
            st.markdown(
                f"""
                <div class='dice-icon-card'>
                  <img src='{svg_data_uri}' width='168' alt='dice-face-{face.cube_id}-{face.face_id}' style='display:block;margin:0 auto;' />
                </div>
                <div class='dice-mini-label'>{html.escape(face.label)}</div>
                """,
                unsafe_allow_html=True,
            )


def _roll_three_faces(state: CollaborativeGameState) -> list[CubeFace]:
    faces_by_cube = list(CUBE_PACKS[state.pack_name].values())
    return [random.choice(face_list) for face_list in faces_by_cube[:3]]


def _animate_roll(state: CollaborativeGameState) -> None:
    placeholder = st.empty()
    for _ in range(10):
        preview_faces = _roll_three_faces(state)
        with placeholder.container():
            st.markdown('<div class="dice-roll-stage">Rolling the dice...</div>', unsafe_allow_html=True)
            _render_faces(preview_faces)
        time.sleep(0.08)

    st.session_state["current_faces"] = _roll_three_faces(state)
    placeholder.empty()


def _render_story_feed(state: CollaborativeGameState, max_items: int = 8) -> None:
    name_map = _player_name_map(state)
    recent = state.contributions[-max_items:]

    if not recent:
        st.info("Story feed will appear here after the first submitted turn.")
        return

    for contribution in recent:
        player_name = name_map.get(contribution.player_id, contribution.player_id)
        initial = player_name[:1].upper() if player_name else "P"
        safe_name = html.escape(player_name)
        safe_text = html.escape(contribution.text)

        st.markdown(
            f"""
            <div class='story-row'>
              <div class='story-avatar'>{initial}</div>
              <div class='story-bubble'>
                <div class='story-name'>{safe_name}</div>
                <p class='story-text'>{safe_text}</p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_side_results(state: CollaborativeGameState, player_name: str) -> None:
    profiles = generate_profiles(state)
    name_map = _player_name_map(state)
    reverse_map = {v: k for k, v in name_map.items()}
    player_id = reverse_map.get(player_name)
    profile = next((p for p in profiles if p.player_id == player_id), None)

    archetype = "In Progress"
    description = "Play your turns to unlock your archetype profile."

    if profile and any(c.player_id == player_id for c in state.contributions):
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


_inject_styles()

for key, value in {
    "game_state": None,
    "play_mode": "local",
    "setup_step": "count",
    "setup_player_count": 2,
    "setup_player_names": ["Player 1", "Player 2"],
    "setup_objective": DEFAULT_OBJECTIVE,
    "setup_rounds": 2,
    "turn_notice": "",
    "mp_room_code": "",
    "mp_player_name": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

query_room = ""
try:
    query_room = str(st.query_params.get("room", "") or "").strip().upper()
except Exception:
    query_room = ""

if query_room and not st.session_state["mp_room_code"]:
    st.session_state["mp_room_code"] = query_room

room_store = None
room_error = None
if st.session_state["play_mode"] == "supabase":
    room_store, room_error = _multiplayer_store_status()

st.radio(
    "Play mode",
    options=["local", "supabase"],
    format_func=lambda mode: "Local single-screen" if mode == "local" else "Multiplayer shared room (Supabase)",
    key="play_mode",
    horizontal=True,
)

_render_brand_header()

if st.session_state["play_mode"] == "supabase":
    if not room_store:
        st.error(room_error or "Supabase is not configured.")
        st.info("Add SUPABASE_URL and SUPABASE_ANON_KEY, then refresh the page.")
        st.stop()

    if not st.session_state["mp_room_code"]:
        st.markdown("<h2 class='screen-subtitle'>Create or join a shared room</h2>", unsafe_allow_html=True)
        tab_create, tab_join = st.tabs(["Create room", "Join room"])

        with tab_create:
            with st.form("create_room_form"):
                host_name = st.text_input("Your nickname", value=st.session_state["mp_player_name"] or "Host")
                expected_players = st.slider("Expected players", min_value=2, max_value=12, value=4)
                objective = st.text_input("Quest objective", value=st.session_state["setup_objective"])
                rounds = st.slider("Rounds", min_value=1, max_value=5, value=int(st.session_state["setup_rounds"]))
                create_room = st.form_submit_button("Create and share room")

            if create_room:
                try:
                    room = room_store.create_room(
                        host_name=host_name,
                        expected_players=int(expected_players),
                        objective=objective,
                        max_rounds=int(rounds),
                        mode=DEFAULT_MODE,
                        pack_name=DEFAULT_PACK,
                    )
                    st.session_state["mp_room_code"] = str(room["room_code"]).upper()
                    st.session_state["mp_player_name"] = host_name.strip()
                    st.session_state["setup_objective"] = objective
                    st.session_state["setup_rounds"] = int(rounds)
                    st.rerun()
                except Exception as exc:
                    st.error(f"Room creation failed: {exc}")

        with tab_join:
            with st.form("join_room_form"):
                join_code = st.text_input("Room code", value=query_room or "").strip().upper()
                join_name = st.text_input("Your nickname", value=st.session_state["mp_player_name"] or "")
                join_room = st.form_submit_button("Join room")

            if join_room:
                try:
                    room_store.join_room(room_code=join_code, player_name=join_name)
                    st.session_state["mp_room_code"] = join_code
                    st.session_state["mp_player_name"] = join_name.strip()
                    st.rerun()
                except Exception as exc:
                    st.error(f"Join failed: {exc}")

        st.stop()

    room_code = st.session_state["mp_room_code"].strip().upper()
    room = room_store.get_room(room_code)

    if not room:
        st.error("Room not found. It may have been deleted.")
        if st.button("Clear room and return"):
            st.session_state["mp_room_code"] = ""
            st.session_state["game_state"] = None
            st.rerun()
        st.stop()

    try:
        st.query_params["room"] = room_code
    except Exception:
        pass

    players = [str(player.get("display_name", "")).strip() for player in room.get("players") or []]
    players = [name for name in players if name]
    player_name = st.session_state["mp_player_name"].strip()

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
                    objective=str(room.get("objective") or DEFAULT_OBJECTIVE),
                    mode=str(room.get("mode") or DEFAULT_MODE),
                    pack_name=str(room.get("pack_name") or DEFAULT_PACK),
                    max_rounds=int(room.get("max_rounds") or 3),
                )
                room_store.update_room(room_code, {"status": "active", "game_state": state.to_record()})
                st.session_state["current_faces"] = []
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

    st.session_state["game_state"] = _state_from_record(game_payload)

if st.session_state["play_mode"] == "local" and st.session_state["game_state"] is None:
    if st.session_state["setup_step"] == "count":
        st.markdown("<h2 class='screen-subtitle'>Select number of players</h2>", unsafe_allow_html=True)
        with st.form("step_count_form"):
            player_count = st.slider("Players", min_value=2, max_value=12, value=int(st.session_state["setup_player_count"]))
            next_step = st.form_submit_button("Next")

        if next_step:
            st.session_state["setup_player_count"] = int(player_count)
            st.session_state["setup_player_names"] = [f"Player {idx + 1}" for idx in range(int(player_count))]
            st.session_state["setup_step"] = "names"
            st.rerun()
        st.stop()

    if st.session_state["setup_step"] == "names":
        st.markdown("<h2 class='screen-subtitle'>Enter nicknames for the players</h2>", unsafe_allow_html=True)

        with st.form("step_names_form"):
            collected_names: list[str] = []
            for idx in range(st.session_state["setup_player_count"]):
                default_name = st.session_state["setup_player_names"][idx]
                name = st.text_input(f"Player {idx + 1}", value=default_name, key=f"player_name_{idx}")
                collected_names.append(name.strip())

            c_back, c_next = st.columns(2)
            go_back = c_back.form_submit_button("Back")
            go_next = c_next.form_submit_button("Next")

        if go_back:
            st.session_state["setup_step"] = "count"
            st.rerun()
        if go_next:
            if any(not player_name for player_name in collected_names):
                st.error("Every player needs a name.")
            else:
                st.session_state["setup_player_names"] = collected_names
                st.session_state["setup_step"] = "start"
                st.rerun()
        st.stop()

    st.markdown("<h2 class='screen-subtitle'>Start the adventure</h2>", unsafe_allow_html=True)
    with st.form("step_start_form"):
        objective = st.text_input("Quest objective", value=st.session_state["setup_objective"])
        rounds = st.slider("Rounds", min_value=1, max_value=5, value=int(st.session_state["setup_rounds"]))
        c_back, c_start = st.columns(2)
        back_to_names = c_back.form_submit_button("Back")
        begin = c_start.form_submit_button("Start game")

    if back_to_names:
        st.session_state["setup_step"] = "names"
        st.rerun()

    if begin:
        st.session_state["setup_objective"] = objective
        st.session_state["setup_rounds"] = int(rounds)
        state = create_game(
            player_names=st.session_state["setup_player_names"],
            objective=objective,
            mode=DEFAULT_MODE,
            pack_name=DEFAULT_PACK,
            max_rounds=int(rounds),
        )
        st.session_state["game_state"] = state
        st.session_state["current_faces"] = []
        st.rerun()
    st.stop()

state = st.session_state.get("game_state")
if not state:
    st.stop()

assert isinstance(state, CollaborativeGameState)

if is_game_finished(state):
    st.markdown("<h2 class='screen-subtitle'>Final Results</h2>", unsafe_allow_html=True)
    profiles_df = _profile_dataframe(state)

    if profiles_df.empty:
        st.info("No completed contributions found yet.")
        st.stop()

    for row in profiles_df.to_dict(orient="records"):
        player = html.escape(str(row["player"]))
        archetype = html.escape(str(row["archetype"]))
        description = html.escape(str(row["description"]))
        icon = player[:1].upper() if player else "P"
        st.markdown(
            f"""
            <div class='final-card'>
              <div class='final-player'>{player}</div>
              <div class='final-row'>
                <div class='final-icon'>{icon}</div>
                <div>
                  <p class='final-archetype'>{archetype}</p>
                  <div class='final-description'>{description}</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    json_path, xlsx_path = _save_collaborative_export(state)
    st.caption(f"Session exported to {json_path.name} and {xlsx_path.name}.")
    st.stop()

active_player = current_player(state)
is_supabase_mode = st.session_state.get("play_mode") == "supabase"
can_play_turn = True
if is_supabase_mode:
    active_nickname = st.session_state.get("mp_player_name", "").strip()
    can_play_turn = bool(active_nickname) and active_player.display_name == active_nickname

if st.session_state.get("turn_notice"):
    st.success(st.session_state["turn_notice"])
    st.session_state["turn_notice"] = ""

st.markdown("<h2 class='screen-subtitle'>Your turn!</h2>", unsafe_allow_html=True)
st.markdown("<div class='screen-note'>Roll the dice and continue the story</div>", unsafe_allow_html=True)

metric_cols = st.columns(4)
metric_cols[0].metric("Round", f"{state.current_round}/{state.max_rounds}")
metric_cols[1].metric("Turn", state.current_turn)
metric_cols[2].metric("Contributions", len(state.contributions))
metric_cols[3].metric("Players", len(state.players))

center = st.columns([1, 1.2, 1])[1]
with center:
    if st.button("ROLL THE DICE", type="primary", disabled=not can_play_turn):
        _animate_roll(state)

if is_supabase_mode and not can_play_turn:
    st.info("Waiting for your turn. Use refresh to sync the latest move.")
    if st.button("Refresh shared game"):
        st.rerun()

faces = st.session_state.get("current_faces", [])
if faces:
    _render_faces(faces)

left, right = st.columns([2.5, 1], gap="large")
with left:
    st.markdown("<h3 class='section-title'>Story So Far</h3>", unsafe_allow_html=True)
    _render_story_feed(state)

with right:
    _render_side_results(state, active_player.display_name)

st.markdown("### Continue the story")
contribution_text = st.text_area("Story block", height=130, placeholder="Enter your text...")

name_map = _player_name_map(state)
other_players = [(p.player_id, p.display_name) for p in state.players if p.player_id != active_player.player_id]
with st.expander("Collaboration options"):
    referenced_ids = st.multiselect(
        "References to previous players",
        options=[pid for pid, _ in other_players],
        format_func=lambda pid: name_map.get(pid, pid),
    )
    included_quiet_player = st.checkbox("Explicitly include a quieter perspective", value=False)

submit_col = st.columns([4, 1])[1]
with submit_col:
    submitted = st.button("Submit", type="primary", disabled=not can_play_turn)

if submitted:
    if not faces:
        st.error("Roll dice first.")
    elif not contribution_text.strip():
        st.error("Story block cannot be empty.")
    else:
        state_to_update = state
        if is_supabase_mode and room_store:
            latest_room = room_store.get_room(st.session_state.get("mp_room_code", ""))
            if not latest_room or not latest_room.get("game_state"):
                st.error("Shared room is unavailable. Refresh and try again.")
                st.stop()

            state_to_update = _state_from_record(latest_room["game_state"])
            active_nickname = st.session_state.get("mp_player_name", "").strip()
            if current_player(state_to_update).display_name != active_nickname:
                st.error("Turn changed while you were writing. Refresh and continue.")
                st.stop()

        review = review_open_story(
            text=contribution_text.strip(),
            rolled_face_labels=[face.label for face in faces],
            referenced_player_ids=referenced_ids,
            included_quiet_player=included_quiet_player,
        )

        submit_contribution(
            state=state_to_update,
            text=contribution_text.strip(),
            rolled_faces=faces,
            referenced_player_ids=referenced_ids,
            included_quiet_player=included_quiet_player,
            manual_score=review.score,
            reviewer_archetype_hint=review.archetype_hint,
        )

        if is_supabase_mode and room_store:
            room_store.update_room(
                st.session_state.get("mp_room_code", ""),
                {
                    "game_state": state_to_update.to_record(),
                    "status": "finished" if is_game_finished(state_to_update) else "active",
                },
            )

        st.session_state["game_state"] = state_to_update
        st.session_state["current_faces"] = []

        if is_game_finished(state_to_update):
            st.session_state["turn_notice"] = "Turn saved. Game complete: final archetypes ready."
        else:
            next_player_name = current_player(state_to_update).display_name
            st.session_state["turn_notice"] = f"Turn saved. Next player: {next_player_name}."
        st.rerun()
