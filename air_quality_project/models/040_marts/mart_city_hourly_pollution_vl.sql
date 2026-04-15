{{ config(materialized='table') }}

SELECT
    city_name,
    pollutant_type,
    measured_at_date,
    measured_hour,
    AVG(measurement_value) AS avg_hourly_pollution,
    COUNT(*) AS nb_measurements
FROM {{ ref('int_station_measurements_vl') }}
GROUP BY
    city_name,
    pollutant_type,
    measured_at_date,
    measured_hour