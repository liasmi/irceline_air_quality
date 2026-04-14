SELECT
    station_id,
    station_label AS station_name,
    SUBSTRING_INDEX(station_label, ' - ', -1) AS city_name,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude
FROM {{ source('raw_source', 'raw_stations') }}