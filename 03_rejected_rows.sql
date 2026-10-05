-- Every rejected row with the FIRST rule it failed, in the same order as pipeline.py:
-- duplicate -> missing campaign -> invalid time -> unknown channel -> negative spend.
DROP VIEW IF EXISTS rejected_rows;
CREATE VIEW rejected_rows AS
WITH numbered AS (
    SELECT
        rowid AS src_row,
        *,
        ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY rowid) AS rn,
        LOWER(TRIM(channel)) AS channel_std
    FROM raw_events
)
SELECT
    event_id, event_time, campaign, channel, spend, clicks,
    CASE
        WHEN rn > 1                                              THEN 'duplicate event_id'
        WHEN campaign IS NULL OR TRIM(campaign) = ''             THEN 'missing campaign'
        WHEN datetime(event_time) IS NULL                        THEN 'invalid event_time'
        WHEN channel_std IS NULL
          OR channel_std NOT IN ('email','social','search','display') THEN 'unknown channel'
        WHEN spend < 0                                           THEN 'negative spend'
    END AS reject_reason
FROM numbered
WHERE rn > 1
   OR campaign IS NULL OR TRIM(campaign) = ''
   OR datetime(event_time) IS NULL
   OR channel_std IS NULL OR channel_std NOT IN ('email','social','search','display')
   OR spend < 0;
