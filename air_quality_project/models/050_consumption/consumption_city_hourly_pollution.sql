{{ config(materialized='table') }}

-- Hourly pollution data by city and pollutant
-- Optional date range filter: set start_date and end_date variables to filter by period
-- If not set, analyzes all historical data

{% set start_date = var('start_date', none) %}
{% set end_date = var('end_date', none) %}

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

{% if start_date and end_date %}
WHERE t.measured_at_date BETWEEN '{{ start_date }}' AND '{{ end_date }}'
{% endif %}

GROUP BY s.city_name, p.pollutant_type, t.hour