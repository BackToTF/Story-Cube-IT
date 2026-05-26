from __future__ import annotations

import random
import re
from typing import Iterable

from .cube_data import CUBE_PACKS, DEFAULT_PACK
from .models import CubeFace


def roll_default_cubes(seed: int | None = None, pack_name: str = DEFAULT_PACK) -> list[CubeFace]:
    return roll_pack_cubes(pack_name=pack_name, seed=seed)


def roll_pack_cubes(pack_name: str, seed: int | None = None) -> list[CubeFace]:
    if pack_name not in CUBE_PACKS:
        raise ValueError(f"Unknown cube pack: {pack_name}")

    rng = random.Random(seed)
    rolled: list[CubeFace] = []
    for cube_name in CUBE_PACKS[pack_name]:
        rolled.append(rng.choice(CUBE_PACKS[pack_name][cube_name]))
    return rolled


def roll_cube_faces(
    cube_name: str,
    count: int = 1,
    seed: int | None = None,
    pack_name: str = DEFAULT_PACK,
) -> list[CubeFace]:
    if pack_name not in CUBE_PACKS:
        raise ValueError(f"Unknown cube pack: {pack_name}")

    if cube_name not in CUBE_PACKS[pack_name]:
        raise ValueError(f"Unknown cube name: {cube_name}")

    if count < 1:
        raise ValueError("count must be >= 1")

    rng = random.Random(seed)
    faces = CUBE_PACKS[pack_name][cube_name]
    return [rng.choice(faces) for _ in range(count)]


def assess_learning_signals(story_text: str, rolled_faces: Iterable[CubeFace]) -> dict[str, int]:
    text = story_text.lower()
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text)

    pipeline_groups = {
        "orchestration": ("adf", "orchestr", "trigger", "dependency", "retry", "sla"),
        "ingestion": ("ingest", "batch", "cdc", "extract", "landing", "source"),
        "transformation": ("databricks", "delta", "transform", "join", "quality", "lineage"),
        "serving": ("dataset", "semantic", "report", "dashboard", "consumer", "access"),
    }
    pipeline_coverage = sum(1 for group in pipeline_groups.values() if any(token in text for token in group))

    inclusion_terms = (
        "inclusion",
        "inclusive",
        "accessibility",
        "bias",
        "representation",
        "multilingual",
        "equity",
        "fair",
        "diverse",
    )
    inclusion_hits = sum(1 for token in inclusion_terms if token in text)
    inclusion_lens = min(inclusion_hits, 3)

    face_alignment = 0
    for face in rolled_faces:
        if face.label.lower() in text:
            face_alignment += 1
    face_alignment = min(face_alignment, 4)

    reflection_depth = 0
    if len(set(words)) >= 25:
        reflection_depth += 1
    if story_text.count(".") + story_text.count(";") >= 2:
        reflection_depth += 1
    if any(token in text for token in ("because", "therefore", "trade-off", "risk", "assumption")):
        reflection_depth += 1

    signal_index = pipeline_coverage + inclusion_lens + face_alignment + reflection_depth

    return {
        "pipeline_coverage": pipeline_coverage,
        "inclusion_lens": inclusion_lens,
        "face_alignment": face_alignment,
        "reflection_depth": reflection_depth,
        "signal_index": signal_index,
    }


def score_story(story_text: str, rolled_faces: Iterable[CubeFace]) -> int:
    # Backward-compatible entrypoint; use the non-competitive team signal index.
    return assess_learning_signals(story_text, rolled_faces)["signal_index"]
