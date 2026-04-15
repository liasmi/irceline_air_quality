{{ config(materialized='table') }}
SELECT *
FROM (
    SELECT
        city_name,
        pollutant_type,
        AVG(measurement_value) AS avg_pollution,
        RANK() OVER (
            PARTITION BY pollutant_type
            ORDER BY AVG(measurement_value) DESC
        ) AS rank_per_pollutant
    FROM {{ ref('int_station_measurements_vl') }}
    GROUP BY city_name, pollutant_type
) ranked
WHERE rank_per_pollutant <= 10