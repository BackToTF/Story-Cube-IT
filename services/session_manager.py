from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import streamlit as st

from services.config import AppConfig


@dataclass
class GameSessionManager:
    state: Any

    @classmethod
    def from_streamlit(cls) -> "GameSessionManager":
        return cls(st.session_state)

    def init_defaults(self, config: AppConfig) -> None:
        defaults = {
            "game_state": None,
            "play_mode": "local",
            "setup_story_mode": config.default_story_mode,
            "setup_step": "count",
            "setup_player_count": 2,
            "setup_player_names": ["Player 1", "Player 2"],
            "setup_objective": config.default_objective,
            "setup_rounds": 2,
            "turn_notice": "",
            "mp_room_code": "",
            "mp_player_name": "",
            "current_faces": [],
        }
        for key, value in defaults.items():
            if key not in self.state:
                self.state[key] = value

    @property
    def game_state(self):
        return self.state.get("game_state")

    @game_state.setter
    def game_state(self, value) -> None:
        self.state["game_state"] = value

    @property
    def play_mode(self) -> str:
        return str(self.state.get("play_mode", "local"))

    @property
    def room_code(self) -> str:
        return str(self.state.get("mp_room_code", "")).strip().upper()

    @room_code.setter
    def room_code(self, value: str) -> None:
        self.state["mp_room_code"] = value.strip().upper()

    @property
    def player_name(self) -> str:
        return str(self.state.get("mp_player_name", "")).strip()

    @player_name.setter
    def player_name(self, value: str) -> None:
        self.state["mp_player_name"] = value.strip()

    @property
    def current_faces(self):
        return self.state.get("current_faces", [])

    @current_faces.setter
    def current_faces(self, faces) -> None:
        self.state["current_faces"] = faces

    def set_notice(self, message: str) -> None:
        self.state["turn_notice"] = message

    def consume_notice(self) -> str:
        message = str(self.state.get("turn_notice", ""))
        self.state["turn_notice"] = ""
        return message
