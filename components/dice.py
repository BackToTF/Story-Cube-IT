from __future__ import annotations

import html
import time
from urllib.parse import quote

import streamlit as st

from story_cube.models import CollaborativeGameState, CubeFace
from story_cube.collaborative_game import roll_phase_face


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
    icon_map = {
        "OnceUpon": "✦",
        "Character": "☺",
        "Setting": "⌂",
        "Event": "➜",
        "Problem": "⚡",
        "Resolution": "❤",
    }
    icon = icon_map.get(face.cube_id, "✧")

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
            <text x='84' y='66' text-anchor='middle' font-family='Nunito Sans, sans-serif' font-size='24' font-weight='800' fill='#0f4c73'>{icon}</text>
            <text x='84' y='92' text-anchor='middle' font-family='Montserrat, sans-serif' font-size='14' font-weight='800' fill='#0f4c73'>{html.escape(label[:11])}</text>
            <text x='84' y='112' text-anchor='middle' font-family='Nunito Sans, sans-serif' font-size='11' font-weight='700' fill='#16486b'>d{face.face_id}</text>
    </svg>
    """


def render_dice_faces(rolled_faces: list[CubeFace]) -> None:
    faces = rolled_faces[:1]
    row = st.columns(max(1, len(faces)))
    for idx, face in enumerate(faces):
        with row[idx]:
            svg_markup = _face_svg(face)
            svg_data_uri = f"data:image/svg+xml;utf8,{quote(svg_markup)}"
            st.markdown(
                f"""
                <div class='dice-icon-card'>
                  <img src='{svg_data_uri}' width='168' alt='dice-face-{face.cube_id}-{face.face_id}' style='display:block;margin:0 auto;' />
                </div>
                """,
                unsafe_allow_html=True,
            )


def animate_dice_roll(state: CollaborativeGameState) -> list[CubeFace]:
    placeholder = st.empty()
    for _ in range(10):
        preview_faces = [roll_phase_face(state)]
        with placeholder.container():
            st.markdown('<div class="dice-roll-stage">Rolling the dice...</div>', unsafe_allow_html=True)
            render_dice_faces(preview_faces)
        time.sleep(0.08)

    final_faces = [roll_phase_face(state)]
    placeholder.empty()
    return final_faces
