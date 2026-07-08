# Story Cube - I&D Edition

Un gioco collaborativo interattivo che trasforma Inclusion and Diversity da concetto astratto a esperienza concreta, attraverso storytelling, gamification e consapevolezza.

## Perche E Importante

L'inclusione non riguarda solo la rappresentazione. Riguarda anche il modo in cui le persone pensano, contribuiscono e collaborano.

Story Cube aiuta i team a:

- Vivere l'inclusione in azione
- Valorizzare stili cognitivi diversi
- Rafforzare la consapevolezza individuale e di gruppo

## Esperienza Di Gioco

I giocatori si alternano nel lanciare dadi tematici e costruiscono insieme una storia condivisa, una fase alla volta.

Ogni contributo e:

- Visibile
- Riconosciuto
- Unico

## Funzionalita Principali

- Storytelling guidato dai dadi con prompt tech e I&D
- Timeline narrativa collaborativa in stile chat
- Scoring multidimensionale:
	- Creativita
	- Coerenza tecnica
	- Inclusivita
	- Collaborazione
- Profilazione archetipica per ogni giocatore
- Modalita multiplayer con stanze condivise su Supabase
- Risultati esportabili di sessione (JSON e XLSX)

## Sistema Di Archetipi (Insight Centrale)

Alla fine di ogni sessione, ogni giocatore riceve un profilo contributivo, per esempio:

- Creative: immaginazione e capacita narrativa
- Logical: pensiero strutturato e analitico
- Empathetic: attenzione alle persone e all'inclusione
- Innovator: approccio originale e fuori dagli schemi
- Connector: capacita di collegare idee e prospettive

L'obiettivo non e la competizione. L'obiettivo e aumentare la consapevolezza personale e del team.

## Come Funziona

1. Seleziona il numero di giocatori.
2. Inserisci i nickname.
3. Lancia il dado.
4. Costruisci la storia in modo collaborativo.
5. Ricevi i profili archetipici finali.

## Schermate

- Setup: ![Setup screen](design/setup_page.png)
- Nickname: ![Nickname screen](design/nickname_setup.png)
- Gioco: ![Game screen](design/gaming_page.png)
- Risultati: ![Results screen](design/results_page.png)

## Stack Tecnologico

- Python 3.14
- Streamlit
- Pandas
- OpenPyXL
- Supabase (persistenza multiplayer)

## Architettura

- `app.py`: UI e orchestrazione
- `src/story_cube/models.py`: entita di dominio
- `src/story_cube/collaborative_game.py`: game loop
- `src/story_cube/scoring.py`: logica di valutazione
- `src/story_cube/archetypes.py`: mappatura dei profili
- `src/story_cube/reviewer_agent.py`: suggerimenti di scoring automatico
- `src/story_cube/multiplayer_store.py`: persistenza delle stanze condivise
- `src/story_cube/cube_data.py`: pacchetti dadi e prompt

## Avvio Rapido

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configurazione Multiplayer

Imposta queste variabili d'ambiente (oppure i segreti Streamlit):

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

Guida completa: `docs/supabase_multiplayer_setup.md`

## Roadmap

- Dashboard facilitatore con insight di team
- Scoring piu evoluto con segnali AI-assisted
- Pacchetti dadi tematici personalizzati
- Report pronti per presentazione
