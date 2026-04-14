SELECT 
    city_name,
    pollutant_type,
    measured_at_date,
    measured_hour,
    AVG(measurement_value) AS avg_hourly_value,
    unit,
    COUNT(*) AS reading_count
FROM {{ ref('int_station_measurements') }}
GROUP BY 1, 2, 3, 4, 6
ORDER BY measured_at_date DESC, measured_hour DESC