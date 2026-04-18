SELECT
   CAST(phenomenon_id AS int) AS phenomenon_id,
    
    CAST(timeseries_id AS int) AS timeseries_id,
    CAST(value AS DECIMAL(10, 4)) AS measurement_value,
    CAST(timestamp AS int) AS timestamp
FROM  {{ source('raw_source', 'raw_measurements') }}
WHERE value IS NOT NULL