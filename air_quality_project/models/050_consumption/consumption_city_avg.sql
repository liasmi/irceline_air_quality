{{ config(materialized='table') }}

SELECT 
    *,
    -- 1. Total stations in this city for this specific pollutant
    COUNT(station_id) OVER(PARTITION BY city_name, pollutant_type) AS city_station_count,
    
    -- 2. The average for the WHOLE city
    AVG(station_avg_pollution) OVER(PARTITION BY city_name, pollutant_type) AS city_wide_avg,
    
    -- 3. The difference (Variance)
    station_avg_pollution - AVG(station_avg_pollution) OVER(PARTITION BY city_name, pollutant_type) AS variance_from_city_avg
FROM (
    -- This is your original 'station_metrics' logic moved into a subquery
    SELECT
        f.station_id,
        s.station_name,
        s.city_name,
        s.latitude,
        s.longitude,
        p.pollutant_type,
        AVG(f.measurement_value) AS station_avg_pollution
    FROM {{ ref('fact_air_quality') }} f
    JOIN {{ ref('dim_station') }} s ON f.station_id = s.station_id
    JOIN {{ ref('dim_pollutant') }} p ON f.phenomenon_id = p.phenomenon_id
    GROUP BY 1, 2, 3, 4, 5, 6
) AS station_metrics_subquery