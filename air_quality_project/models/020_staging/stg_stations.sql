SELECT
    CAST(station_id AS int) AS station_id,
    CAST(station_label AS VARCHAR(255)) AS station_name,
    TRIM(SUBSTRING(station_label, LOCATE('-', station_label) + 1)) AS city_name,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude
FROM {{ source('raw_source', 'raw_stations') }}