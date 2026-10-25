-- Run this in the Supabase SQL Editor (Dashboard -> SQL Editor -> New query).
-- It creates one table for generated itineraries.

create extension if not exists "pgcrypto";

create table if not exists public.itineraries (
  id uuid primary key default gen_random_uuid(),
  destination text not null,
  start_date date not null,
  end_date date not null,
  budget numeric(12, 2) not null,
  interests text[] not null default '{}',
  trip_days integer not null,
  daily_budget numeric(12, 2) not null,
  source text not null check (source in ('ai', 'sample')),
  days jsonb not null,
  tips text[] not null default '{}',
  created_at timestamptz not null default now()
);

create index if not exists itineraries_created_at_idx
  on public.itineraries (created_at desc);

-- For a beginner demo, allow the backend key to read and insert rows.
-- If you use the anon key, these policies are required.
alter table public.itineraries enable row level security;

drop policy if exists "Allow insert itineraries" on public.itineraries;
create policy "Allow insert itineraries"
  on public.itineraries
  for insert
  to anon, authenticated
  with check (true);

drop policy if exists "Allow read itineraries" on public.itineraries;
create policy "Allow read itineraries"
  on public.itineraries
  for select
  to anon, authenticated
  using (true);
