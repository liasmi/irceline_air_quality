{{ config(materialized='table') }}

SELECT DISTINCT
    timestamp,
    from_unixtime(CAST(timestamp AS UNSIGNED) / 1000) AS measured_at_timestamp,
    DATE(FROM_UNIXTIME(CAST(timestamp AS UNSIGNED) / 1000)) AS measured_at_date,
    HOUR(FROM_UNIXTIME(CAST(timestamp AS UNSIGNED) / 1000)) AS hour
FROM {{ ref('stg_measurements') }}