SELECT
    CASE 
        WHEN CAST(phenomenon_id AS CHAR) = '5' THEN 'PM10'
        WHEN CAST(phenomenon_id AS CHAR) = '6001' THEN 'PM2.5'
        WHEN CAST(phenomenon_id AS CHAR) = '1' THEN 'NO2'
        WHEN CAST(phenomenon_id AS CHAR) = '8' THEN 'CO2'
        WHEN CAST(phenomenon_id AS CHAR) = '7' THEN 'SO2'
        ELSE 'UNKNOWN'
    END AS pollutant_type,
    
    CAST(timeseries_id AS CHAR) AS timeseries_id,
    CAST(value AS DECIMAL(10, 4)) AS measurement_value,
    
    -- MySQL Timestamp conversion from Unix milliseconds
    FROM_UNIXTIME(CAST(timestamp AS UNSIGNED) / 1000) AS measured_at_timestamp,
    DATE(FROM_UNIXTIME(CAST(timestamp AS UNSIGNED) / 1000)) AS measured_at_date
FROM  {{ source('raw_source', 'raw_measurements') }}
WHERE value IS NOT NULL