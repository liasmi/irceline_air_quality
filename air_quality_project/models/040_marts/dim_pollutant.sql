{{ config(materialized='table') }}

SELECT DISTINCT
    phenomenon_id,
    phenomenon_name,
    abbreviation AS pollutant_type
FROM {{ ref('stg_phenomena') }}
WHERE abbreviation IN ('PM10', 'PM2.5', 'NO2', 'CO2', 'SO2')