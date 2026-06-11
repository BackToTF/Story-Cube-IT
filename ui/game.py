from __future__ import annotations

import html
import re

import streamlit as st

from components.dice import animate_dice_roll, render_dice_faces
from services.config import AppConfig
from services.game_service import compose_story_text, evaluate_contribution, get_player_name_map
from services.session_manager import GameSessionManager
from story_cube.archetypes import build_player_profile
from story_cube.collaborative_game import can_intervene, current_player, is_game_finished, submit_contribution
from story_cube.scoring import aggregate_player_dimension_averages


PHASE_LABELS = {
    "once_upon_a_time": "C'era una volta",
    "who": "Chi",
    "where": "Dove",
    "what": "Cosa succede",
    "problem": "Problema",
    "resolution": "Risoluzione",
}

PHASE_GUIDANCE = {
    "once_upon_a_time": "Inizia la storia con calma e semplicità.",
    "who": "Scegli chi c'è nella storia.",
    "where": "Scegli dove si svolge la scena.",
    "what": "Scegli cosa accade in questa fase.",
    "problem": "Scegli il problema o la sfida.",
    "resolution": "Scegli come si risolve la situazione.",
}

UI_TEXT_TRANSLATIONS = {
    "Once upon a time": "C'era una volta",
    "One sunny morning": "Una mattina di sole",
    "Far away in a small place": "Lontano, in un posto piccolo",
    "A quiet day began": "Iniziò una giornata tranquilla",
    "Someone woke up smiling": "Qualcuno si svegliò sorridendo",
    "The story opened with a surprise": "La storia iniziò con una sorpresa",
    "A happy world": "Un mondo felice",
    "A curious world": "Un mondo curioso",
    "A magical world": "Un mondo magico",
    "A simple hello": "Un semplice ciao",
    "A small adventure": "Una piccola avventura",
    "A gentle mystery": "Un mistero gentile",
    "A child spoke": "Parlò un bambino",
    "A friend listened": "Un amico ascoltò",
    "A soft wind answered": "Un vento leggero rispose",
    "A tiny idea": "Una piccola idea",
    "A brave wish": "Un desiderio coraggioso",
    "A little question": "Una piccola domanda",
}


def _phase_label(phase: str) -> str:
    return PHASE_LABELS.get(phase, phase.replace("_", " ").title())


def _it(text: str) -> str:
    return UI_TEXT_TRANSLATIONS.get(text, text)


def _resolve_player_id(state, display_name: str) -> str:
    match = next((player.player_id for player in state.players if player.display_name == display_name), None)
    return match or display_name


def _normalize_story_text(text: str) -> str:
    if "<" not in text and ">" not in text:
        return text
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = html.unescape(cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _render_phase_banner(state) -> None:
    phase = state.story_phase
    st.markdown(f"<h2 class='screen-subtitle'>{_phase_label(phase)}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='screen-note'>{PHASE_GUIDANCE.get(phase, 'Continua la storia.')}</div>", unsafe_allow_html=True)


def _render_sidebar_context(state, active_display_name: str) -> None:
    name_map = get_player_name_map(state)
    st.sidebar.markdown("### Storia Finora")
    recent = state.contributions[-8:]
    if not recent:
        st.sidebar.caption("La storia apparirà qui dopo la prima fase.")
    else:
        for contribution in recent:
            contributor_id = contribution.intervening_player_id or contribution.player_id
            author = name_map.get(contributor_id, contributor_id)
            phase = _phase_label(contribution.story_phase)
            badge = "IO C'ERO" if contribution.is_intervention else "Turno"
            st.sidebar.markdown(f"**{author}** · {phase} · {badge}")
            st.sidebar.caption(_normalize_story_text(contribution.text))

    averages = aggregate_player_dimension_averages(state.contributions)
    reverse_map = {display: pid for pid, display in name_map.items()}
    active_player_id = reverse_map.get(active_display_name)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Profilo Turno")
    if active_player_id and active_player_id in averages:
        profile = build_player_profile(active_player_id, averages[active_player_id])
        st.sidebar.markdown(f"**{active_display_name}**")
        st.sidebar.caption(profile.dominant_archetype)
        st.sidebar.caption(profile.description)
    else:
        st.sidebar.caption("Completa qualche fase per vedere il profilo archetipico.")


def _render_face_selection(state, manager: GameSessionManager, room_store) -> None:
    rolled_faces = manager.current_faces
    active_face = rolled_faces[0] if rolled_faces else None

    if not active_face:
        st.info("Lancia il dado per sbloccare le opzioni.")
        return

    st.markdown(f"<div class='dice-mini-label'>{_it(active_face.label)}</div>", unsafe_allow_html=True)
    st.caption(_it(active_face.prompt))

    choice_key = f"selected_option_{state.game_id}_{state.current_turn}"
    text_key = f"custom_text_{state.game_id}_{state.current_turn}"
    if choice_key not in st.session_state:
        st.session_state[choice_key] = ""

    choices = active_face.options[:3] if active_face.options else [active_face.prompt]
    choices = [_it(choice) for choice in choices]
    cols = st.columns(3)
    for idx, option in enumerate(choices):
        with cols[idx]:
            is_selected = st.session_state[choice_key] == option
            label = f"🎲 {option}"
            if is_selected:
                label = f"✅ {option}"
            if st.button(label, key=f"pick_{state.game_id}_{state.current_turn}_{idx}", use_container_width=True):
                st.session_state[choice_key] = option
                st.rerun()

    selected_option = st.session_state.get(choice_key, "")
    if selected_option:
        st.success(f"Hai scelto: {selected_option}")

    custom_text = st.text_area(
        "Aggiunta facoltativa (1-2 frasi)",
        placeholder="Puoi aggiungere una frase breve, oppure lasciare vuoto.",
        height=90,
        key=text_key,
    )

    referenced_player_ids: list[str] = []
    included_quiet_player = False
    if state.game_mode == "advanced":
        with st.expander("Opzioni avanzate", expanded=False):
            name_map = get_player_name_map(state)
            active = current_player(state)
            other_players = [
                (player.player_id, player.display_name)
                for player in state.players
                if player.player_id != active.player_id
            ]
            referenced_player_ids = st.multiselect(
                "Riferisci un altro giocatore",
                options=[player_id for player_id, _ in other_players],
                format_func=lambda player_id: name_map.get(player_id, player_id),
            )
            included_quiet_player = st.checkbox("Includi anche una voce più silenziosa", value=False)

    can_submit = bool(selected_option)
    if st.button("Conferma fase", type="primary", disabled=not can_submit):
        if custom_text and len(custom_text.split()) > 20 and state.game_mode == "basic":
            st.warning("In modalità Basic tieni il testo molto corto.")
            st.stop()

        selected_options = [selected_option]
        contribution_text = compose_story_text(selected_options, custom_text)
        review = evaluate_contribution(
            text=contribution_text,
            rolled_face_labels=[active_face.label],
            referenced_player_ids=referenced_player_ids,
            included_quiet_player=included_quiet_player,
            story_phase=state.story_phase,
            selected_options=selected_options,
        )

        submit_contribution(
            state=state,
            text=contribution_text,
            rolled_faces=[active_face],
            referenced_player_ids=referenced_player_ids,
            included_quiet_player=included_quiet_player,
            selected_options=selected_options,
            custom_text=custom_text,
            story_phase=state.story_phase,
            manual_score=review.score,
            reviewer_archetype_hint=review.archetype_hint,
        )

        if manager.play_mode == "supabase" and room_store:
            room_store.update_room(
                manager.room_code,
                {
                    "game_state": state.to_record(),
                    "status": "finished" if is_game_finished(state) else "active",
                },
            )

        st.session_state[choice_key] = ""
        manager.current_faces = []

        if is_game_finished(state):
            manager.set_notice("Storia completata. I profili finali sono pronti.")
        else:
            manager.set_notice(f"Fase salvata. Prossimo giocatore: {current_player(state).display_name}.")
        st.rerun()


def _render_intervention_panel(state, manager: GameSessionManager, room_store) -> None:
    player_id = _resolve_player_id(state, manager.player_name)
    if not player_id or not can_intervene(state, player_id):
        return

    with st.expander("IO C'ERO!", expanded=False):
        st.caption("Aggiungi un punto di vista breve senza interrompere il turno principale.")
        intervention_text = st.text_area(
            "Intervento breve",
            placeholder="Esempio: secondo me manca il punto di vista di chi usa il gioco.",
            height=80,
            key=f"intervention_{state.game_id}_{state.current_turn}",
        )
        send_intervention = st.button("Invia IO C'ERO", type="secondary")

    if not send_intervention:
        return

    if not intervention_text.strip():
        st.error("Scrivi prima un intervento breve.")
        return

    if len(intervention_text.split()) > 24 and state.game_mode == "basic":
        st.warning("In modalità Basic mantieni gli interventi molto brevi.")
        return

    review = evaluate_contribution(
        text=intervention_text.strip(),
        rolled_face_labels=[],
        referenced_player_ids=[],
        included_quiet_player=False,
        story_phase=state.story_phase,
        selected_options=[],
        is_intervention=True,
        intervening_player_id=player_id,
    )

    submit_contribution(
        state=state,
        text=intervention_text.strip(),
        rolled_faces=[],
        referenced_player_ids=[],
        included_quiet_player=False,
        selected_options=[],
        custom_text=intervention_text.strip(),
        story_phase=state.story_phase,
        is_intervention=True,
        intervening_player_id=player_id,
        manual_score=review.score,
        reviewer_archetype_hint=review.archetype_hint,
    )

    if room_store:
        room_store.update_room(
            manager.room_code,
            {
                "game_state": state.to_record(),
                "status": "finished" if is_game_finished(state) else "active",
            },
        )

    manager.set_notice("Intervento IO C'ERO salvato.")
    st.rerun()


def render_game_screen(manager: GameSessionManager, config: AppConfig, room_store, state_from_record_fn) -> None:
    state = manager.game_state
    if not state:
        st.stop()

    if manager.play_mode == "supabase" and room_store and manager.room_code:
        room = room_store.get_room(manager.room_code)
        if room and room.get("game_state"):
            state = state_from_record_fn(room["game_state"], config)
            manager.game_state = state

    active_player = current_player(state)
    if manager.play_mode == "local" and not manager.player_name:
        manager.player_name = active_player.display_name

    is_my_turn = manager.play_mode == "local" or (bool(manager.player_name) and active_player.display_name == manager.player_name)

    notice = manager.consume_notice()
    if notice:
        st.success(notice)

    _render_phase_banner(state)
    _render_sidebar_context(state, manager.player_name or active_player.display_name)

    cards = [
        ("Round", f"{state.current_round}/{state.max_rounds}"),
        ("Turno", str(state.current_turn)),
        ("Fase", _phase_label(state.story_phase)),
        ("Modalità", state.game_mode.title()),
        ("Giocatori", str(len(state.players))),
    ]
    card_cols = st.columns(5)
    for idx, (title, value) in enumerate(cards):
        with card_cols[idx]:
            st.markdown(
                f"""
                <div class='status-card'>
                  <div class='status-title'>{title}</div>
                  <div class='status-value'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(f"Fase corrente: {_phase_label(state.story_phase)}")

    if is_my_turn:
        turn_cols = st.columns([1, 1.1, 1])
        with turn_cols[1]:
            if st.button("LANCIA IL DADO", type="primary"):
                manager.current_faces = animate_dice_roll(state)
                selection_key = f"selected_option_{state.game_id}_{state.current_turn}"
                st.session_state[selection_key] = ""
                st.rerun()
    else:
        st.info(f"In attesa del turno di {active_player.display_name}.")

    if manager.current_faces:
        render_dice_faces(manager.current_faces)

    if is_my_turn:
        _render_face_selection(state, manager, room_store)
    else:
        st.caption("Puoi comunque contribuire con IO C'ERO.")

    _render_intervention_panel(state, manager, room_store)
