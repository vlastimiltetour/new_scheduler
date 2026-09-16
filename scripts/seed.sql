-- scripts/seed.sql

-- Enable UUID extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- 0. DROP ALL EXISTING TABLES (Cleans up previous schema & data completely)
DROP TABLE IF EXISTS interview CASCADE;
DROP TABLE IF EXISTS timeslot CASCADE;
DROP TABLE IF EXISTS person CASCADE;
-- 1. CREATE TABLES (Matching SQLAlchemy Imperative Mapping schema)

CREATE TABLE IF NOT EXISTS person (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    person_type VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS timeslot (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    owner_id UUID REFERENCES person(id) ON DELETE CASCADE,
    owner_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS interview (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate UUID NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    interviewer UUID NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    timeslot TIMESTAMP NOT NULL
);


-- 2. INSERT SEED DATA

-- Persons (2 candidates, 3 interviewers)
INSERT INTO person (id, name, email, person_type) 
VALUES 
    ('ffe91d06-6061-4f96-9364-bac9de72ab98', 'Alan Harper', 'alan@harper.com', 'candidate'),
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Carl Uberinterviewer', 'carl@everpure.com', 'interviewer'),
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'Johnny Cage', 'johnny@cage.com', 'interviewer'),
    ('c3d4e5f6-a7b8-9012-cdef-234567890123', 'Sonia Blade', 'sonia@specialforces.gov', 'interviewer'),
    ('d4e5f6a7-b8c9-0123-def0-345678901234', 'Jake Harper', 'jake@harper.com', 'candidate')
ON CONFLICT (email) DO NOTHING;


-- Timeslots (2 WEEKS: April 6, 2026 – April 17, 2026)
INSERT INTO timeslot (id, start_time, end_time, owner_id, owner_type, status)
VALUES 
    -- WEEK 1
    (gen_random_uuid(), '2026-04-06 09:00:00', '2026-04-06 13:00:00', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-06 09:00:00', '2026-04-06 11:00:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-06 10:00:00', '2026-04-06 12:00:00', 'c3d4e5f6-a7b8-9012-cdef-234567890123', 'interviewer', 'unavailable'),

    (gen_random_uuid(), '2026-04-07 13:00:00', '2026-04-07 16:00:00', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-07 14:00:00', '2026-04-07 15:30:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'interviewer', 'unavailable'),

    (gen_random_uuid(), '2026-04-08 09:00:00', '2026-04-08 12:00:00', 'ffe91d06-6061-4f96-9364-bac9de72ab98', 'candidate',   'unavailable'),
    (gen_random_uuid(), '2026-04-08 11:00:00', '2026-04-08 14:00:00', 'c3d4e5f6-a7b8-9012-cdef-234567890123', 'interviewer', 'unavailable'),

    (gen_random_uuid(), '2026-04-09 10:00:00', '2026-04-09 11:30:00', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-09 10:00:00', '2026-04-09 11:30:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-09 11:00:00', '2026-04-09 13:00:00', 'c3d4e5f6-a7b8-9012-cdef-234567890123', 'interviewer', 'unavailable'),

    (gen_random_uuid(), '2026-04-10 09:00:00', '2026-04-10 10:00:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-10 09:30:00', '2026-04-10 10:30:00', 'd4e5f6a7-b8c9-0123-def0-345678901234', 'candidate',   'unavailable'),

    -- WEEK 2
    (gen_random_uuid(), '2026-04-13 11:00:00', '2026-04-13 15:00:00', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-13 13:00:00', '2026-04-13 16:00:00', 'c3d4e5f6-a7b8-9012-cdef-234567890123', 'interviewer', 'unavailable'),

    (gen_random_uuid(), '2026-04-14 09:00:00', '2026-04-14 14:00:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-14 12:00:00', '2026-04-14 16:00:00', 'ffe91d06-6061-4f96-9364-bac9de72ab98', 'candidate',   'unavailable'),

    (gen_random_uuid(), '2026-04-15 09:00:00', '2026-04-15 11:00:00', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-15 10:30:00', '2026-04-15 12:30:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-15 12:00:00', '2026-04-15 14:00:00', 'c3d4e5f6-a7b8-9012-cdef-234567890123', 'interviewer', 'unavailable'),

    (gen_random_uuid(), '2026-04-16 14:00:00', '2026-04-16 16:00:00', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'interviewer', 'unavailable'),

    (gen_random_uuid(), '2026-04-17 12:00:00', '2026-04-17 16:00:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'interviewer', 'unavailable'),
    (gen_random_uuid(), '2026-04-17 13:00:00', '2026-04-17 16:00:00', 'c3d4e5f6-a7b8-9012-cdef-234567890123', 'interviewer', 'unavailable')
ON CONFLICT DO NOTHING;