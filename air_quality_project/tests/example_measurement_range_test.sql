-- Example: Standalone test using the custom measurement_value_in_range macro
-- Location: tests/example_measurement_range_test.sql
-- 
-- This test checks if any measurement values in the staging model fall outside
-- the acceptable range (0-500) or contain NULL values.
-- 
-- To run this specific test:
-- dbt test --select test_measurement_value_in_range_example

{{ config(
    severity = 'error',
    tags = ['data_quality']
) }}

SELECT *
FROM {{ ref('fact_air_quality') }}
WHERE measurement_value < 0
   OR measurement_value > 500
   OR measurement_value IS NULL
