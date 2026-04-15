WITH city_hourly AS (
    SELECT * FROM {{ ref('int_station_measurements_vl') }}
),

-- EU annual limit values (µg/m³)
-- Note: MySQL 8.0 syntax for CTE with VALUES
pollution_thresholds AS (
    SELECT 'pm10' AS phenomenon, 40.0 AS threshold_value
    UNION ALL SELECT 'pm25', 25.0
    UNION ALL SELECT 'no2', 40.0
    UNION ALL SELECT 'so2', 20.0
    UNION ALL SELECT 'co2', 1800.0
),

-- Average per city per phenomenon
city_phenomenon_avg AS (
    SELECT
        city_name AS city,
        LOWER(pollutant_type) AS phenomenon,
        unit AS unit_of_measure,
        AVG(measurement_value) AS mean_concentration,
        COUNT(DISTINCT measured_at_date) AS days_observed
    FROM city_hourly
    GROUP BY 1, 2, 3
),

-- Normalize by EU threshold
city_normalized AS (
    SELECT
        cpa.*,
        pt.threshold_value,
        (cpa.mean_concentration / pt.threshold_value) AS normalized_score
    FROM city_phenomenon_avg cpa
    JOIN pollution_thresholds pt ON cpa.phenomenon = pt.phenomenon
),

-- Composite score calculation
city_composite AS (
    SELECT
        city,
        AVG(normalized_score) AS composite_pollution_score,
        MAX(CASE WHEN phenomenon = 'pm10' THEN mean_concentration END) AS avg_pm10,
        MAX(CASE WHEN phenomenon = 'pm25' THEN mean_concentration END) AS avg_pm25,
        MAX(CASE WHEN phenomenon = 'no2'  THEN mean_concentration END) AS avg_no2,
        MAX(CASE WHEN phenomenon = 'co2'  THEN mean_concentration END) AS avg_co2,
        MAX(CASE WHEN phenomenon = 'so2'  THEN mean_concentration END) AS avg_so2,
        MAX(days_observed) AS days_observed
    FROM city_normalized
    GROUP BY city
),

-- Ranking logic for MySQL
ranked_cities AS (
    SELECT
        RANK() OVER (ORDER BY composite_pollution_score DESC) AS pollution_rank,
        city,
        ROUND(composite_pollution_score, 4) AS composite_pollution_score,
        ROUND(avg_pm10, 2) AS avg_pm10,
        ROUND(avg_pm25, 2) AS avg_pm25,
        ROUND(avg_no2, 2) AS avg_no2,
        ROUND(avg_co2, 2) AS avg_co2,
        ROUND(avg_so2, 2) AS avg_so2,
        days_observed
    FROM city_composite
)

SELECT * FROM ranked_cities 
WHERE pollution_rank <= 10
ORDER BY pollution_rank;