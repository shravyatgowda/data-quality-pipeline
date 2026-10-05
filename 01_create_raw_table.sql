-- Raw landing table for the messy event log (SQLite-compatible).
-- Load the CSV with the SQLite shell:
--   .mode csv
--   .import --skip 1 data/raw_events.csv raw_events
-- (Everything is stored as TEXT/REAL exactly as received. No cleaning here.)
DROP TABLE IF EXISTS raw_events;
CREATE TABLE raw_events (
    event_id    INTEGER,
    event_time  TEXT,
    campaign    TEXT,
    channel     TEXT,
    spend       REAL,
    clicks      REAL
);
