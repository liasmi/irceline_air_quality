{{ config(materialized='table') }}

SELECT
    city_name,
    COUNT(DISTINCT station_id) AS nb_stations

FROM {{ ref('dim_station') }}

GROUP BY city_name