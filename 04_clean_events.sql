-- Clean events: de-duplicated, standardised, validated. Missing clicks become 0.
DROP VIEW IF EXISTS clean_events;
CREATE VIEW clean_events AS
WITH numbered AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY rowid) AS rn,
        LOWER(TRIM(channel)) AS channel_std
    FROM raw_events
)
SELECT
    event_id,
    datetime(event_time)        AS event_time,
    campaign,
    channel_std                 AS channel,
    spend,
    COALESCE(clicks, 0)         AS clicks
FROM numbered
WHERE rn = 1
  AND campaign IS NOT NULL AND TRIM(campaign) <> ''
  AND datetime(event_time) IS NOT NULL
  AND channel_std IN ('email','social','search','display')
  AND spend >= 0;
