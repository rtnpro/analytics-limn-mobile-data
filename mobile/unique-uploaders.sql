SELECT
    DATE_FORMAT(CONCAT(Month.month, '01'), '%Y-%m-%d') AS Month,
    COALESCE(Android.count, 0) AS Android,
    COALESCE(iOS.count, 0) AS iOS,
    COALESCE(Web.count, 0) AS Web

-- http://stackoverflow.com/a/6871220/365238
-- ... using MariaDB 10 SEQUENCE engine instead of information_schema.columns
FROM (
    SELECT EXTRACT(YEAR_MONTH FROM SUBDATE(CURDATE(), INTERVAL @num:=@num+1 MONTH)) AS month
    FROM seq_1_to_12, (SELECT @num:=-1) num LIMIT 12
) AS Month

LEFT JOIN (
    SELECT EXTRACT(YEAR_MONTH FROM timestamp) AS month, COUNT(DISTINCT event_username) AS count
    FROM {{ tables.upload_attempts }}
    WHERE
        event_platform LIKE 'Android%' AND
        event_result = 'success' AND
        wiki = 'commonswiki'
    GROUP BY month
    ORDER BY month DESC
    LIMIT 12
) AS Android ON Month.month = Android.month

LEFT JOIN (
    SELECT EXTRACT(YEAR_MONTH FROM timestamp) AS month, COUNT(DISTINCT event_username) AS count
    FROM {{ tables.upload_attempts }}
    WHERE
        event_platform LIKE 'iOS%' AND
        event_result = 'success' AND
        wiki = 'commonswiki'
    GROUP BY month
    ORDER BY month DESC
    LIMIT 12
) AS iOS ON Month.month = iOS.month

LEFT JOIN (
    SELECT EXTRACT(YEAR_MONTH FROM timestamp) AS month, COUNT(DISTINCT event_username) AS count
    FROM {{ tables.upload_web }}
    WHERE
        event_action = 'success' AND
        wiki != 'testwiki'
    GROUP BY month
    ORDER BY month DESC
    LIMIT 12
) AS Web ON Month.month = Web.month;
