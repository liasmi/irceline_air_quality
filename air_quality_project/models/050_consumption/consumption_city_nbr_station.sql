SELECT
    t.city_name,
    t.pollutant_type,
    t.avg_pollution,
    s.nb_stations
FROM mart_top10_polluted_cities t
JOIN mart_city_station_summary s
    ON t.city_name = s.city_name