{{ config(materialized='view') }}

SELECT
    m.measured_at_timestamp,
    m.measured_at_date,
    HOUR(m.measured_at_timestamp) AS measured_hour,
    m.pollutant_type,
    m.measurement_value,
    t.unit,
    s.city_name,
    s.station_name,
    s.station_id,
    s.latitude,
    s.longitude
FROM {{ ref('stg_measurements') }} m
JOIN {{ ref('stg_timeseries') }} t 
    ON m.timeseries_id = t.timeseries_id
JOIN {{ ref('stg_stations') }} s 
    ON t.station_id = s.station_id