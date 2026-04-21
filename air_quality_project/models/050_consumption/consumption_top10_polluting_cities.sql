{{ config(materialized='table') }}

-- Top 10 polluting cities by pollutant type
-- Optional date range filter: set start_date and end_date variables to filter by period
-- If not set, analyzes all historical data

{% set start_date = var('start_date', none) %}
{% set end_date = var('end_date', none) %}

SELECT
    cp.city_name,
    cp.pollutant_type,
    cp.avg_pollution
FROM (
    SELECT
        s.city_name,
        p.pollutant_type,
        AVG(f.measurement_value) AS avg_pollution
    FROM {{ ref('fact_air_quality') }} f
    JOIN {{ ref('dim_pollutant') }} p
        ON f.phenomenon_id = p.phenomenon_id
    JOIN {{ ref('dim_station') }} s
        ON f.station_id = s.station_id
    {% if start_date and end_date %}
    JOIN {{ ref('dim_time') }} t
        ON f.timestamp = t.timestamp
    WHERE t.measured_at_date BETWEEN '{{ start_date }}' AND '{{ end_date }}'
    {% endif %}
    GROUP BY s.city_name, p.pollutant_type
) cp
LEFT JOIN (
    SELECT
        s.city_name,
        p.pollutant_type,
        AVG(f.measurement_value) AS avg_pollution
    FROM {{ ref('fact_air_quality') }} f
    JOIN {{ ref('dim_pollutant') }} p
        ON f.phenomenon_id = p.phenomenon_id
    JOIN {{ ref('dim_station') }} s
        ON f.station_id = s.station_id
    {% if start_date and end_date %}
    JOIN {{ ref('dim_time') }} t
        ON f.timestamp = t.timestamp
    WHERE t.measured_at_date BETWEEN '{{ start_date }}' AND '{{ end_date }}'
    {% endif %}
    GROUP BY s.city_name, p.pollutant_type
) cp2
    ON cp.pollutant_type = cp2.pollutant_type
    AND cp2.avg_pollution > cp.avg_pollution
GROUP BY
    cp.city_name,
    cp.pollutant_type,
    cp.avg_pollution
HAVING COUNT(cp2.city_name) < 10
ORDER BY
    cp.pollutant_type,
    cp.avg_pollution DESC