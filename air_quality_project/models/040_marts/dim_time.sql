{{ config(materialized='table') }}

SELECT DISTINCT
    measured_at_timestamp,
    DATE(measured_at_timestamp) AS date,
    HOUR(measured_at_timestamp) AS hour
FROM {{ ref('stg_measurements') }}