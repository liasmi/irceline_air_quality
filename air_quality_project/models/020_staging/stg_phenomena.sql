SELECT
    CAST(phenomenon_id AS int) AS phenomenon_id,
    label AS phenomenon_name,
    CASE 
        WHEN phenomenon_id = '5' THEN 'PM10'
        WHEN phenomenon_id = '6001' THEN 'PM2.5'
        WHEN phenomenon_id = '8' THEN 'NO2'
        WHEN phenomenon_id = '71' THEN 'CO2'
        WHEN phenomenon_id = '1' THEN 'SO2'
        ELSE 'OTHER'
    END AS abbreviation
FROM {{ source('raw_source', 'raw_phenomena') }}
