# Story Cube - I&D Edition

An interactive collaborative game that transforms Inclusion and Diversity from concept into lived experience through storytelling, gamification, and self-awareness.

## Why It Matters

Inclusion is not only about representation. It is also about how people think, contribute, and collaborate.

Story Cube helps teams:

- Experience inclusion in action
- Value different cognitive styles
- Build individual and team awareness

## Core Experience

Players take turns rolling three thematic dice (tech and inclusion prompts) and collaboratively build a shared story.

Each contribution is:

- Visible
- Valued
- Uniquely different

## Key Features

- Dice-driven storytelling with tech and I&D prompts
- Collaborative narrative timeline with chat-like flow
- Multi-dimensional scoring:
	- Creativity
	- Technical coherence
	- Inclusivity
	- Collaboration
- Archetype profiling for each player
- Multiplayer mode with Supabase shared rooms
- Exportable session results (JSON and XLSX)

## Archetype System (Core Insight)

At the end of each session, every player receives a contribution profile such as:

- Creative: imagination and storytelling
- Logical: structured and analytical thinking
- Empathetic: focus on people and inclusion
- Innovator: out-of-the-box thinking
- Connector: linking ideas and perspectives

The goal is not competition. The goal is self-awareness and team awareness.

## How It Works

1. Select number of players.
2. Enter nicknames.
3. Roll the dice.
4. Build the story collaboratively.
5. Receive archetype profiles.

## Screens

- Setup: ![Setup screen](design/setup_page.png)
- Nicknames: ![Nickname screen](design/nickname_setup.png)
- Game: ![Game screen](design/gaming_page.png)
- Results: ![Results screen](design/results_page.png)

## Tech Stack

- Python 3.14
- Streamlit
- Pandas
- OpenPyXL
- Supabase (multiplayer persistence)

## Architecture

- `app.py`: UI and orchestration
- `src/story_cube/models.py`: domain entities
- `src/story_cube/collaborative_game.py`: game loop
- `src/story_cube/scoring.py`: evaluation logic
- `src/story_cube/archetypes.py`: profile mapping
- `src/story_cube/reviewer_agent.py`: automated scoring hints
- `src/story_cube/multiplayer_store.py`: shared room persistence
- `src/story_cube/cube_data.py`: dice packs and prompts

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Multiplayer Setup

Set these environment variables (or Streamlit secrets):

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

Full guide: `docs/supabase_multiplayer_setup.md`

## Roadmap

- Facilitator dashboard with team insights
- Smarter scoring with AI-assisted signals
- Custom themed dice packs
- Presentation-ready reports
