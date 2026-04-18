{{ config(materialized='table') }}

SELECT
    CONCAT(m.timeseries_id, '_', m.timestamp) AS measurement_id,

    m.timestamp,
    t.station_id,
    t.phenomenon_id,

    m.measurement_value

FROM {{ ref('stg_measurements') }} m

JOIN {{ ref('stg_timeseries') }} t
    ON m.timeseries_id = t.timeseries_id

JOIN {{ ref('stg_stations') }} s
    ON t.station_id = s.station_id

JOIN {{ ref('dim_pollutant') }} p
    ON t.phenomenon_id = p.phenomenon_id

