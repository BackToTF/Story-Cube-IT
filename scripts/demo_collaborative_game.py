from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from story_cube.collaborative_game import (
    create_game,
    current_player,
    generate_profiles,
    is_game_finished,
    roll_turn_faces,
    submit_contribution,
)


def _sample_text(player_name: str, face_labels: list[str]) -> str:
    return (
        f"{player_name} builds on previous idea using {', '.join(face_labels)}. "
        "In ADF we orchestrate ingestion, transform in Databricks, and ensure accessibility and fairness in outputs."
    )


def run_demo() -> None:
    game = create_game(
        player_names=["Arianna", "Luca", "Maya", "Samir", "Elena"],
        objective="Build a data pipeline story that includes underrepresented user needs.",
        max_rounds=2,
    )

    while not is_game_finished(game):
        player = current_player(game)
        faces = roll_turn_faces(game)
        text = _sample_text(player.display_name, [face.label for face in faces])
        reference_ids = []
        if game.contributions:
            reference_ids = [game.contributions[-1].player_id]

        contribution = submit_contribution(
            state=game,
            text=text,
            rolled_faces=faces,
            referenced_player_ids=reference_ids,
            included_quiet_player=(game.current_turn % 4 == 0),
        )
        print(
            f"Turn {contribution.turn_index} | Player {player.display_name} | "
            f"Score total {contribution.score.total if contribution.score else 0:.2f}"
        )

    profiles = generate_profiles(game)
    print("\nFinal archetypes:")
    for profile in profiles:
        print(f"- {profile.player_id}: {profile.dominant_archetype} -> {profile.description}")


if __name__ == "__main__":
    run_demo()
