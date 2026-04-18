SELECT
    CAST(timeseries_id AS int) AS timeseries_id,
    CAST(station_id AS int) AS station_id,
    CAST(phenomenon_id AS int) AS phenomenon_id,
    CAST(uom AS VARCHAR(255)) AS unit
FROM {{ source('raw_source', 'raw_timeseries') }}