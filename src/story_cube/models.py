from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class CubeFace:
    cube_id: str
    face_id: int
    label: str
    prompt: str


@dataclass(frozen=True)
class Player:
    player_id: str
    display_name: str


@dataclass(frozen=True)
class ContributionScore:
    creativity: float
    technical_coherence: float
    inclusivity_awareness: float
    collaboration: float

    @property
    def total(self) -> float:
        return (
            self.creativity
            + self.technical_coherence
            + self.inclusivity_awareness
            + self.collaboration
        )


@dataclass(frozen=True)
class StoryContribution:
    contribution_id: str
    player_id: str
    turn_index: int
    round_index: int
    created_at: datetime
    rolled_faces: list[CubeFace]
    text: str
    referenced_player_ids: list[str] = field(default_factory=list)
    included_quiet_player: bool = False
    score: ContributionScore | None = None


@dataclass(frozen=True)
class PlayerProfile:
    player_id: str
    dominant_archetype: str
    description: str
    dimension_averages: dict[str, float]


@dataclass
class CollaborativeGameState:
    game_id: str
    mode: str
    objective: str
    pack_name: str
    players: list[Player]
    max_rounds: int
    current_round: int = 1
    current_turn: int = 1
    contributions: list[StoryContribution] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_record(self) -> dict[str, Any]:
        return {
            "game_id": self.game_id,
            "mode": self.mode,
            "objective": self.objective,
            "pack_name": self.pack_name,
            "max_rounds": self.max_rounds,
            "current_round": self.current_round,
            "current_turn": self.current_turn,
            "created_at": self.created_at.isoformat(),
            "players": [
                {
                    "player_id": p.player_id,
                    "display_name": p.display_name,
                }
                for p in self.players
            ],
            "contributions": [
                {
                    "contribution_id": c.contribution_id,
                    "player_id": c.player_id,
                    "turn_index": c.turn_index,
                    "round_index": c.round_index,
                    "created_at": c.created_at.isoformat(),
                    "text": c.text,
                    "referenced_player_ids": c.referenced_player_ids,
                    "included_quiet_player": c.included_quiet_player,
                    "rolled_faces": [
                        {
                            "cube_id": f.cube_id,
                            "face_id": f.face_id,
                            "label": f.label,
                            "prompt": f.prompt,
                        }
                        for f in c.rolled_faces
                    ],
                    "score": {
                        "creativity": c.score.creativity,
                        "technical_coherence": c.score.technical_coherence,
                        "inclusivity_awareness": c.score.inclusivity_awareness,
                        "collaboration": c.score.collaboration,
                        "total": c.score.total,
                    }
                    if c.score
                    else None,
                }
                for c in self.contributions
            ],
        }


@dataclass
class GameSession:
    mode: str
    players: int
    rolled_faces: list[CubeFace]
    story_text: str = ""
    score: int = 0
    session_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_record(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "mode": self.mode,
            "players": self.players,
            "score": self.score,
            "story_text": self.story_text,
            "rolled_faces": [
                {
                    "cube_id": f.cube_id,
                    "face_id": f.face_id,
                    "label": f.label,
                    "prompt": f.prompt,
                }
                for f in self.rolled_faces
            ],
        }
