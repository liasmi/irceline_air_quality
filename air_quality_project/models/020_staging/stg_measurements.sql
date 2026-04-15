SELECT
   CAST(phenomenon_id AS int) AS phenomenon_id,
    
    CAST(timeseries_id AS int) AS timeseries_id,
    CAST(value AS DECIMAL(10, 4)) AS measurement_value,
    
    -- MySQL Timestamp conversion from Unix milliseconds
    FROM_UNIXTIME(CAST(timestamp AS UNSIGNED) / 1000) AS measured_at_timestamp,
    DATE(FROM_UNIXTIME(CAST(timestamp AS UNSIGNED) / 1000)) AS measured_at_date
FROM  {{ source('raw_source', 'raw_measurements') }}
WHERE value IS NOT NULL