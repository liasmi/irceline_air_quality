SELECT
    timeseries_id AS timeseries_id,
    station_id,
    -- Mapping phenomenon IDs back to names for the business side
    CASE 
        WHEN phenomenon_id = '5' THEN 'PM10'
        WHEN phenomenon_id = '6001' THEN 'PM2.5'
        WHEN phenomenon_id = '1' THEN 'NO2'
        WHEN phenomenon_id = '8' THEN 'CO2'
        WHEN phenomenon_id = '7' THEN 'SO2'
        ELSE 'OTHER'
    END AS pollutant_type,
    uom AS unit
FROM {{ source('raw_source', 'raw_timeseries') }}