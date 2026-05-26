from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from story_cube.engine import assess_learning_signals, roll_default_cubes, score_story


def test_roll_default_cubes_returns_pack_faces() -> None:
    rolled = roll_default_cubes(seed=42)
    assert len(rolled) == 4


def test_score_story_non_negative() -> None:
    rolled = roll_default_cubes(seed=42)
    score = score_story(
        "ADF trigger starts ingestion. Databricks transforms data with quality checks and inclusion lens.",
        rolled,
    )
    assert score >= 0


def test_assess_learning_signals_contains_expected_keys() -> None:
    rolled = roll_default_cubes(seed=42)
    signals = assess_learning_signals(
        "ADF orchestrates ingest. Databricks transforms to semantic dataset with accessibility checks.",
        rolled,
    )
    assert "pipeline_coverage" in signals
    assert "inclusion_lens" in signals
    assert "signal_index" in signals
