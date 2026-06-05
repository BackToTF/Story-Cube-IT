# PROJECT_HISTORY — Story Cube - I&D

Session handoff log for Story Cube - Inclusion and Diversity Edition

Last update: 2026-06-04

---

## Project Purpose

Story Cube - I&D e un gioco collaborativo progettato per workshop aziendali, che combina:

- storytelling guidato da prompt tech
- meccaniche di inclusione attiva
- riflessione sui diversi stili cognitivi nel team

### Obiettivi principali

- Favorire partecipazione inclusiva (anche di profili non tecnici)
- Valorizzare diversi approcci (logico, creativo, empatico)
- Creare un'esperienza coinvolgente e memorabile
- Generare output strutturati (profili e insight di team)

---

## Core Gameplay

- I partecipanti lanciano 3 dadi tematici (tech + I&D)
- Costruiscono una storia collaborativa a turni
- I contributi vengono registrati in una timeline condivisa (chat-like)

### Dimensioni di valutazione

Ogni contributo e valutato su:

- Creativita
- Coerenza tecnica
- Inclusivita
- Collaborazione

Il sistema evita bias premiando diversi stili di contributo.

---

## Archetype System

Al termine del gioco, ogni partecipante riceve:

- Un archetipo dominante
- Una breve descrizione del proprio stile nel team

Esempi:

- Logical
- Creative
- Connector
- Innovator
- Facilitator
- Analytical
- Empathetic

Il gioco diventa uno strumento di self-awareness e team awareness.

---

## Current Architecture

- Frontend: app.py (Streamlit)
- Domain logic: src/story_cube/

### Moduli principali

- models.py -> struttura dati
- collaborative_game.py -> game loop
- scoring.py -> valutazione multi-dimensionale
- archetypes.py -> mapping profili
- reviewer_agent.py -> scoring automatizzato
- cube_data.py -> contenuto dei dadi

### Output

- Export JSON
- Export XLSX (timeline + profili utenti)

---

## Recent Updates (2026-06-04)

- Introdotto visual design immersivo in Streamlit
- Migliorata UX dei dadi con simboli evocativi
- Revisione prompt per essere piu inclusivi e meno tecnici
- Attivato reviewer automatico in tutte le modalita
- Inserita logica archetipica come output finale del gioco

---

## Contribute-Back Policy

Il progetto segue un approccio di miglioramento continuo:

- Identificazione pattern riutilizzabili
- Documentazione in lessons_learned.md
- Separazione tra reusable patterns e project-specific elements

---

## Sessione 2 — 2026-06-04

### Obiettivo

Classificazione pattern e aggiornamento knowledge base.

### Attivita

- Analisi log e file di progetto
- Deduplicazione pattern
- Classificazione reusable vs specifici

### Output

- 1 pattern reusable identificato
- 1 pattern project-specific documentato

---

## Key Patterns

- Prompt Metaphorization for Non-Technical Facilitation
- Mirrored Dice Visual Ritual (project-specific)

---

## Design Principles

- Inclusione by design
- Non-competitivita (safe workshop environment)
- Bilanciamento tra tecnico e creativo
- Semplicita per favorire engagement
