-- Reporting queries on top of the cleaned data and the reject log.

-- 1. Rows kept vs rejected
SELECT
    (SELECT COUNT(*) FROM raw_events)   AS input_rows,
    (SELECT COUNT(*) FROM clean_events) AS clean_rows,
    (SELECT COUNT(*) FROM rejected_rows) AS rejected_rows;

-- 2. Rejected rows by reason
SELECT reject_reason, COUNT(*) AS rows_rejected
FROM rejected_rows
GROUP BY reject_reason
ORDER BY rows_rejected DESC;

-- 3. Clean spend and clicks by channel, with each channel's share of total spend
SELECT
    channel,
    COUNT(*)                         AS events,
    ROUND(SUM(spend), 2)             AS total_spend,
    SUM(clicks)                      AS total_clicks,
    ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER (), 1) AS spend_share_pct
FROM clean_events
GROUP BY channel
ORDER BY total_spend DESC;
