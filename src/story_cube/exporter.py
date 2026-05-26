from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .models import GameSession


def export_session(
    session: GameSession,
    output_dir: str | Path = "data/sessions",
    learning_signals: dict[str, int] | None = None,
) -> tuple[Path, Path]:
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    json_path = base_dir / f"{session.session_id}.json"
    xlsx_path = base_dir / f"{session.session_id}.xlsx"

    record = session.to_record()
    if learning_signals:
        record["learning_signals"] = learning_signals

    with json_path.open("w", encoding="utf-8") as fp:
        json.dump(record, fp, indent=2)

    face_rows = record["rolled_faces"]
    df = pd.DataFrame(face_rows)
    summary = pd.DataFrame(
        [
            {
                "session_id": record["session_id"],
                "created_at": record["created_at"],
                "mode": record["mode"],
                "players": record["players"],
                "score": record["score"],
                "story_text": record["story_text"],
                "signal_index": (learning_signals or {}).get("signal_index"),
                "pipeline_coverage": (learning_signals or {}).get("pipeline_coverage"),
                "inclusion_lens": (learning_signals or {}).get("inclusion_lens"),
                "face_alignment": (learning_signals or {}).get("face_alignment"),
                "reflection_depth": (learning_signals or {}).get("reflection_depth"),
            }
        ]
    )
    signals = pd.DataFrame([learning_signals or {}])

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="summary", index=False)
        df.to_excel(writer, sheet_name="faces", index=False)
        signals.to_excel(writer, sheet_name="signals", index=False)

    return json_path, xlsx_path
