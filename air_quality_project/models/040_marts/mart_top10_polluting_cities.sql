SELECT 
    city_name,
    pollutant_type,
    AVG(measurement_value) AS avg_value,
    unit,
    COUNT(DISTINCT station_id) AS total_stations,
    MAX(measured_at_timestamp) AS last_observed_at
FROM {{ ref('int_station_measurements') }}
GROUP BY city_name, pollutant_type, unit
ORDER BY avg_value DESC
LIMIT 10