SELECT 
    city_name,
    station_name,
    station_id,
    latitude,
    longitude,
    -- List all pollutants this specific station is capable of tracking
    GROUP_CONCAT(DISTINCT pollutant_type ORDER BY pollutant_type SEPARATOR ', ') AS pollutants_tracked,
    -- Total volume of data contributed by this station
    COUNT(*) AS total_measurements_contributed
FROM {{ ref('int_station_measurements_vl') }}
GROUP BY 1, 2, 3, 4, 5
ORDER BY city_name, station_name