{% test measurement_value_in_range(model, column_name, min_value=0, max_value=500) %}
{# 
  Generic test to validate that measurement values fall within an acceptable range.
  
  Args:
    model: The model to test
    column_name: The column containing measurement values
    min_value: Minimum acceptable value (default: 0)
    max_value: Maximum acceptable value (default: 500)
  
  This test checks for values outside the specified range, which likely indicates
  data quality issues or sensor errors.
#}

SELECT *
FROM {{ model }}
WHERE {{ column_name }} < {{ min_value }}
   OR {{ column_name }} > {{ max_value }}
   OR {{ column_name }} IS NULL

{% endtest %}
