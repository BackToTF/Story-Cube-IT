from __future__ import annotations

import html
import re

import streamlit as st

from story_cube.models import CollaborativeGameState


def _normalize_story_text(text: str) -> str:
    if "<" not in text and ">" not in text:
        return text
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = html.unescape(cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def render_story_timeline(state: CollaborativeGameState, player_name_map: dict[str, str], max_items: int = 8) -> None:
    recent = state.contributions[-max_items:]

    if not recent:
        st.info("Story feed will appear here after the first submitted turn.")
        return

    for contribution in recent:
        player_name = player_name_map.get(contribution.player_id, contribution.player_id)
        initial = player_name[:1].upper() if player_name else "P"
        safe_name = html.escape(player_name)
        safe_text = html.escape(_normalize_story_text(contribution.text))
        phase_label = html.escape(contribution.story_phase.replace("_", " ").title())
        selected_options = "".join(
            f"<span class='story-option-chip'>{html.escape(option)}</span>" for option in contribution.selected_options
        )
        intervention_label = ""
        if contribution.is_intervention:
            intervener = player_name_map.get(contribution.intervening_player_id or "", contribution.intervening_player_id or "")
            intervention_label = f"<div class='story-badge'>IO C'ERO! {html.escape(intervener or 'Guest')}</div>"
            if intervener:
                safe_name = f"{safe_name} <span style='font-size:0.9rem;color:#1d4ed8;'>(intervention)</span>"

        st.markdown(
            f"""
            <div class='story-row'>
              <div class='story-avatar'>{initial}</div>
              <div class='story-bubble {'intervention' if contribution.is_intervention else ''}'>
                {intervention_label}
                <div class='story-name'>{safe_name}</div>
                <div class='story-meta'>{phase_label}</div>
                <p class='story-text'>{safe_text}</p>
                <div class='story-options'>{selected_options}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
