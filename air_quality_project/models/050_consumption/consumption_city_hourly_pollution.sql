{{ config(materialized='table') }}

SELECT
    s.city_name,
    p.pollutant_type,
    t.measured_at_date,
    t.hour,
    AVG(f.measurement_value) AS avg_hourly_pollution

FROM {{ ref('fact_air_quality') }} f

JOIN {{ ref('dim_pollutant') }} p
    ON f.phenomenon_id = p.phenomenon_id

JOIN {{ ref('dim_station') }} s
    ON f.station_id = s.station_id

JOIN {{ ref('dim_time') }} t
    ON f.timestamp = t.timestamp

GROUP BY s.city_name, p.pollutant_type, t.hour