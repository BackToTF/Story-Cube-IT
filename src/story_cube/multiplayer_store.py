from __future__ import annotations

from datetime import datetime, timezone
from random import choices
from string import ascii_uppercase, digits
from typing import Any

try:
    from supabase import Client, create_client
except ImportError as exc:  # pragma: no cover - handled at runtime in app
    Client = Any  # type: ignore[assignment]
    create_client = None  # type: ignore[assignment]
    SUPABASE_IMPORT_ERROR = str(exc)
else:
    SUPABASE_IMPORT_ERROR = ""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SupabaseRoomStore:
    def __init__(self, url: str, anon_key: str, table_name: str = "storycube_rooms") -> None:
        if not create_client:
            raise RuntimeError(
                "supabase package is not installed. Add 'supabase' to requirements and redeploy."
            )
        self.client: Client = create_client(url, anon_key)
        self.table_name = table_name

    @staticmethod
    def generate_room_code(length: int = 6) -> str:
        alphabet = ascii_uppercase + digits
        return "".join(choices(alphabet, k=length))

    def get_room(self, room_code: str) -> dict[str, Any] | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("room_code", room_code.upper())
            .limit(1)
            .execute()
        )
        if not result.data:
            return None
        return result.data[0]

    def create_room(
        self,
        host_name: str,
        expected_players: int,
        objective: str,
        max_rounds: int,
        mode: str,
        pack_name: str,
        game_mode: str,
    ) -> dict[str, Any]:
        room_code = self.generate_room_code()
        player_name = host_name.strip()
        if not player_name:
            raise ValueError("Host name is required.")

        payload = {
            "room_code": room_code,
            "status": "lobby",
            "expected_players": int(expected_players),
            "objective": objective,
            "max_rounds": int(max_rounds),
            "mode": mode,
            "game_mode": game_mode,
            "pack_name": pack_name,
            "host_name": player_name,
            "players": [{"display_name": player_name}],
            "game_state": None,
            "updated_at": _utc_now_iso(),
        }

        created = self.client.table(self.table_name).insert(payload).execute()
        if not created.data:
            raise RuntimeError("Room creation failed.")
        return created.data[0]

    def join_room(self, room_code: str, player_name: str) -> dict[str, Any]:
        normalized_code = room_code.upper().strip()
        clean_name = player_name.strip()
        if not normalized_code:
            raise ValueError("Room code is required.")
        if not clean_name:
            raise ValueError("Player name is required.")

        room = self.get_room(normalized_code)
        if not room:
            raise ValueError("Room not found.")
        if room.get("status") != "lobby":
            raise ValueError("Room already started.")

        players = list(room.get("players") or [])
        lower_names = {str(p.get("display_name", "")).lower() for p in players}
        if clean_name.lower() in lower_names:
            raise ValueError("This nickname is already used in the room.")

        expected_players = int(room.get("expected_players") or 0)
        if expected_players and len(players) >= expected_players:
            raise ValueError("Room is already full.")

        players.append({"display_name": clean_name})
        updated = self.update_room(normalized_code, {"players": players})
        if not updated:
            raise RuntimeError("Unable to join room.")
        return updated

    def update_room(self, room_code: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        payload = dict(patch)
        payload["updated_at"] = _utc_now_iso()

        result = (
            self.client.table(self.table_name)
            .update(payload)
            .eq("room_code", room_code.upper())
            .execute()
        )
        if not result.data:
            return None
        return result.data[0]
