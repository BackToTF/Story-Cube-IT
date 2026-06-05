# Story Cube IT - Inclusion and Diversity

Story Cube IT is a custom game to build creativity for data and AI-era skills such as orchestration thinking, collaboration, and inclusive decision making.

## Project structure

- app.py: Streamlit app entrypoint
- src/story_cube/: game engine and domain modules
- data/sessions/: exported game sessions (JSON and XLSX)
- data/templates/: CSV templates for group setup and feedback
- assets/: cube icons or visual assets
- assets/mockups/story-cube-it-facilitator-view.svg: facilitator-focused mockup
- assets/dice/it-dice-pack-spec.md: spec for real IT-themed dice graphics
- docs/architecture-story-cube-tech-inclusion.md: modular architecture and game design
- tests/: engine smoke tests
- scripts/run.ps1: convenience script to run the app
- scripts/demo_collaborative_game.py: basic collaborative game simulation
- guidelines.md: base gameplay ideas

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   - pip install -r requirements.txt
3. Run the app:
   - streamlit run app.py

## MVP game loop

1. Select a game mode.
2. Define the mandatory round objective (message-first).
3. Roll cubes.
4. Write story or idea.
5. Assess non-competitive learning signals and export session KPI.

## Interactive Demo Flow (Multiplayer)

1. Configure 5-20 players and rounds.
2. Start a new interactive game session.
3. For each turn, the active player gets 3 dice faces.
4. Submit contribution with optional references to other players.
5. Review live timeline and per-contribution signals.
6. At end game, review archetypes and export JSON/XLSX report.

## Suggested next steps

- Add custom cube packs by theme (security, data, UX, sustainability).
- Add timed rounds and team leaderboard.
- Add PPT export for workshop recap.

## Team workflow for the pilot

1. Use docs/game-mechanics-decision-matrix.md to pick primary mechanic and fallback.
2. Assign roles with data/templates/group_work_template.csv.
3. Dry run the activity using docs/session-runbook.md.
4. Run live session and collect feedback in data/templates/session_feedback_template.csv.
5. Capture improvements in docs/next-meeting-agenda.md for follow-up.
