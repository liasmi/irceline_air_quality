{{ config(materialized='view') }}

SELECT
    t.timeseries_id,
    m.measured_at_timestamp,
    m.measured_at_date,
    HOUR(m.measured_at_timestamp) AS measured_hour,
    p.abbreviation AS pollutant_type,
    m.measurement_value,
    t.unit,
    s.city_name,
    s.station_name,
    s.station_id,
    s.latitude,
    s.longitude
FROM {{ ref('stg_measurements') }} m
Inner JOIN {{ ref('stg_timeseries') }} t 
    ON m.timeseries_id = t.timeseries_id
Inner JOIN {{ ref('stg_stations') }} s 
    ON t.station_id = s.station_id
Inner JOIN {{ ref('stg_phenomena') }} p
    ON CAST(t.phenomenon_id AS CHAR) = CAST(p.phenomenon_id AS CHAR)
WHERE
    s.latitude BETWEEN 50.68 AND 51.51
    AND s.longitude BETWEEN 2.54 AND 5.92
    AND p.abbreviation IN ('PM10', 'PM2.5', 'NO2', 'CO2', 'SO2')