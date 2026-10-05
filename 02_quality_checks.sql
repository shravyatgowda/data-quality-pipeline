-- Profile the raw data: how many rows break each validation rule?
-- Each rule is counted independently, so a row that breaks two rules is counted twice.
-- The rejected_rows view assigns each row only its first failed rule.
SELECT 'total rows'                  AS check_name, COUNT(*) AS rows_affected FROM raw_events
UNION ALL
SELECT 'duplicate event_id (extra copies)', COUNT(*) - COUNT(DISTINCT event_id) FROM raw_events
UNION ALL
SELECT 'missing campaign', COUNT(*) FROM raw_events
 WHERE campaign IS NULL OR TRIM(campaign) = ''
UNION ALL
SELECT 'invalid event_time', COUNT(*) FROM raw_events
 WHERE datetime(event_time) IS NULL
UNION ALL
SELECT 'unknown channel (after trim/lower)', COUNT(*) FROM raw_events
 WHERE LOWER(TRIM(channel)) NOT IN ('email','social','search','display')
    OR channel IS NULL
UNION ALL
SELECT 'negative spend', COUNT(*) FROM raw_events WHERE spend < 0
UNION ALL
SELECT 'missing clicks (filled with 0)', COUNT(*) FROM raw_events WHERE clicks IS NULL;
