{{ config(materialized='table') }}

SELECT
    city_name,
    COUNT(DISTINCT station_id) AS nb_stations,

    GROUP_CONCAT(
        CONCAT(
            station_id, '|',
            station_name, '|',
            latitude, '|',
            longitude
        )
        SEPARATOR ';'
    ) AS stations

FROM {{ ref('int_station_measurements_vl') }}
GROUP BY city_name