from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from story_cube.collaborative_game import (
    create_game,
    generate_profiles,
    is_game_finished,
    roll_turn_faces,
    submit_contribution,
)


def test_collaborative_game_loop_generates_profiles() -> None:
    game = create_game(
        player_names=["P1", "P2", "P3", "P4", "P5"],
        objective="Build a fair data pipeline story",
        max_rounds=1,
    )

    while not is_game_finished(game):
        faces = roll_turn_faces(game, seed=42)
        submit_contribution(
            state=game,
            text=(
                "ADF orchestrates batch ingestion, Databricks transforms data, and accessibility checks "
                "protect underrepresented users."
            ),
            rolled_faces=faces,
            referenced_player_ids=["P1"],
            included_quiet_player=True,
        )

    profiles = generate_profiles(game)
    assert len(profiles) == 5
    assert all(profile.dominant_archetype for profile in profiles)
