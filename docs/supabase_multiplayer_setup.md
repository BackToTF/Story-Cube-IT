# Supabase Multiplayer Setup

This app uses a single table (`storycube_rooms`) to store lobby and game state.

## 1. Create table (Supabase SQL Editor)

```sql
create table if not exists public.storycube_rooms (
  room_code text primary key,
  status text not null default 'lobby',
  expected_players int not null default 4,
  objective text not null,
  max_rounds int not null default 3,
  mode text not null default 'collaborative',
  pack_name text not null default 'data_pipeline_id',
  host_name text not null,
  players jsonb not null default '[]'::jsonb,
  game_state jsonb null,
  updated_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index if not exists idx_storycube_rooms_status on public.storycube_rooms (status);
```

## 2. RLS policies (simple MVP)

If you are using anonymous key only, you can start with open policies for MVP testing:

```sql
alter table public.storycube_rooms enable row level security;

create policy "storycube_rooms_select"
  on public.storycube_rooms
  for select
  using (true);

create policy "storycube_rooms_insert"
  on public.storycube_rooms
  for insert
  with check (true);

create policy "storycube_rooms_update"
  on public.storycube_rooms
  for update
  using (true)
  with check (true);
```

For production, tighten these policies and use authenticated users.

## 3. Streamlit secrets

In Streamlit Cloud (or local `.streamlit/secrets.toml`):

```toml
SUPABASE_URL = "https://YOUR-PROJECT.supabase.co"
SUPABASE_ANON_KEY = "YOUR_ANON_KEY"
```

## 4. Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Use `Play mode -> Multiplayer shared room (Supabase)` to create/join rooms.
