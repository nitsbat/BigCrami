import bq_helper
open_aq = bq_helper.BigQueryHelper(active_project = "bigquery-public-data",dataset_name = "openaq")
open_aq.list_tables()
# output will be ['global_air_quality']

open_aq.head("global_air_quality")
query = """ select city from `bigquery-public-data.openaq.global_air_quality` where country = 'US' """

open_aq.estimate_query_size(query)
# output will be 0.0003067702054977417

us_cities = open_aq.query_to_pandas_safe(query)
us_cities.head()

us_cities.city.value_counts().head()
open_aq.table_schema("global_air_quality")

query1 = """ select country from `bigquery-public-data.openaq.global_air_quality` 
             where unit != 'ppm'   """
open_aq.estimate_query_size(query1)
result = open_aq.query_to_pandas_safe(query1)

result.head()
result.country.value_counts()
# Total number of countries using unit other than 'ppm' are 64. 

query1 = """ select distinct country,unit from `bigquery-public-data.openaq.global_air_quality` 
             where unit != 'ppm' order by country"""
open_aq.query_to_pandas_safe(query1)

query2 = """ SELECT pollutant FROM `bigquery-public-data.openaq.global_air_quality` WHERE value=0 """
open_aq.estimate_query_size(query2)
result2 = open_aq.query_to_pandas_safe(query2)
result2.head()

result2.pollutant.value_counts()
query = """ select distinct pollutant,value
            from `bigquery-public-data.openaq.global_air_quality` where value = 0 order by pollutant """
# Only 6 pollutants with value = 0

open_aq.query_to_pandas_safe(query)
# the final result will be
"""
pollutant	value
0	bc	0.0
1	co	0.0
2	no2	0.0
3	o3	0.0
4	pm10	0.0
5	pm25	0.0
6	so2	0.0
"""