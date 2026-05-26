# Story Cube - Tech & Inclusion Edition: Architecture

## 1) Modular architecture

## Prototype target

- Frontend: Streamlit (single-page collaborative facilitator UI)
- Backend domain layer: Python modules in src/story_cube
- Persistence: JSON/XLSX export for hackathon; optional SQLite/PostgreSQL later

## Modules

- game_engine
  - Dice rolling
  - Turn management
  - Round progression
- contribution_timeline
  - Append-only contributions timeline (chat-like)
  - Turn metadata and references
- scoring_service
  - Multi-dimensional scoring per contribution
  - Non-binary, flexible scale
- archetype_service
  - Aggregate per-player dimensions
  - Map to dominant archetype + profile summary
- reporting_service
  - Export session timeline, scores, archetypes

## Scalability path

1. Keep domain pure (no UI dependency)
2. Expose REST/WebSocket API later if moving to web multiplayer
3. Replace local export with DB + analytics warehouse when needed

## 2) Data structures

## Player

- player_id: string
- display_name: string

## Dice and faces

- cube_id: string (e.g., Orchestration, Ingestion)
- face_id: int
- label: string
- prompt: string

## Story contribution

- contribution_id: string
- player_id: string
- turn_index: int
- round_index: int
- created_at: datetime
- rolled_faces: CubeFace[]
- text: string
- referenced_player_ids: string[]
- included_quiet_player: bool
- score: ContributionScore

## Scoring

- creativity: float (0-5)
- technical_coherence: float (0-5)
- inclusivity_awareness: float (0-5)
- collaboration: float (0-5)
- total: computed float

## 3) Game loop (step by step)

1. Facilitator creates game session:
- objective
- player list (5-20)
- max rounds
- dice pack

2. For each turn:
- identify current player
- roll 3 dice faces
- player submits contribution text
- optional references to previous players
- optional quiet-player inclusion flag
- score contribution across 4 dimensions
- append to timeline

3. End of round:
- rotate to next round after all players have contributed
- show interim team signals without ranking people

4. End of game:
- aggregate per-player dimension averages
- map to dominant archetype
- generate personal style summary
- export report

## 4) Scoring strategy

## Recommended prototype strategy: Rule-based heuristics + optional AI assist

- Rule-based core:
  - deterministic, transparent, easy to tune
  - dimensions scored by lexical and structural signals
- Optional AI-assist (later):
  - LLM reviewer proposes dimension adjustments in bounded range
  - guardrails to prevent harsh or biased scoring

## Anti-bias controls

- no single dimension dominates final profile
- collaboration/inclusion signals can offset low technical verbosity
- quiet-player inclusion bonus at team-level behavior

## 5) Archetype mapping

Use averaged dimensions and threshold rules:

- Logical: high technical + solid inclusion
- Creative: high creativity
- Connector: high collaboration and references
- Innovator: high creativity + above-average technical
- Facilitator: balanced profile with collaboration support
- Analytical: very high technical/detail orientation
- Empathetic: high inclusion + high collaboration

## 6) Optional enhancements

- Live timeline UI with color tags per dimension
- "Reference someone" UI shortcut to encourage collaborative linking
- Participation heatmap to identify silent players early
- End-game radar chart per player
- Session comparison dashboard over time
- Export profile cards for workshop debrief

## 7) First implementation in repository

Implemented modules:

- src/story_cube/models.py
- src/story_cube/scoring.py
- src/story_cube/archetypes.py
- src/story_cube/collaborative_game.py

Current prototype supports:

- multi-player turn loop
- contribution timeline
- multi-dimensional scoring
- archetype assignment at game end
