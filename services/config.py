from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    default_mode: str = "collaborative"
    default_story_mode: str = "basic"
    default_pack: str = "storybook_simple"
    default_objective: str = (
        "Build a surreal IT adventure that still keeps a plausible "
        "data-stack backbone and inclusive impact."
    )
