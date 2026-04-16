{{ config(materialized='table') }}

SELECT
    station_id,
    station_name,
    city_name,
    latitude,
    longitude
FROM {{ ref('stg_stations') }}