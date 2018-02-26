# BigCrami
The project aims at handling Big Data Queries in python.Though packages like Pandas and Numpy have high level data structures and manipulation tools to make data analysis easier, there are not preferrable when dealing with BigQueries (appx 3-4 TB of data) as the queries take vast amount of time for execution.

## BigQuery and SQL

BigQuery is a Google Cloud product for storing and accessing huge databases very quickly. You can find a lot of BigQuery datasets in the  internet but the best platform to apply it is via [KAGGLE](https://www.kaggle.com).
SQL is the third most popular language for data science and easiest way to access these data in the datasets.For many databases out there, SQL is the only way to access the information in them.

##### NOTE : Because the datasets on BigQuery can be very large, there are some restrictions on how much data you can access. Each Kaggle user can scan 5TB every 30 days for free. If you go over your quota you're going to have to wait for it to reset.

## Software Requirements
* KAGGLE Account
* bq_helper - Helper package to simplify common read-only BigQuery tasks.

              >> import bq_helper as bq_helper

## Introduction and Basics

We are performing queries in [Hacker News dataset](https://www.kaggle.com/hacker-news/hacker-news).The addresses of BigQuery datasets look like this:

![l11gdkx](https://user-images.githubusercontent.com/22686274/36656719-a066d610-1aef-11e8-992f-f3cea36d6c19.png)

We will need to pass this information to BigQueryHelper in order to create our helper object. The active_project argument takes the BigQuery info, which is currently "bigquery-public-data" for all the BigQuery datasets on Kaggle. The dataset_name argument takes the name of the dataset we've added to our query. In this case it's "hacker_news".The following code will create our BigQueryHelper object:

      >> hacker_news = bq_helper.BigQueryHelper(active_project= "bigquery-public-data", 
                                       dataset_name = "hacker_news")

### Checking out the structure of your dataset

First thing anyone wants to do is check the schema and to know whether the data is structured or not. BigQueryHelper.list_tables() will print all the tables in our dataset

     # print a list of all the tables in the hacker_news dataset
     >>hacker_news.list_tables()
     
     # print information on all the columns in the "full" table
     # in the hacker_news dataset
     >> hacker_news.table_schema("full")
     
Each SchemaField tells us about a specific column. In order, the information is:

* The name of the column
* The datatype in the column
* The mode of the column (NULLABLE means that a column allows NULL values, and is the default)
* A description of the data in that column

Simliarly `hacker_new.head()` will print the first ten entries. The more powerful command related to .head() is 

      # preview the first ten entries in the by column of the full table
      hacker_news.head("full", selected_columns="by", num_rows=10)

The output of the above command will look like : 

![capture](https://user-images.githubusercontent.com/22686274/36657081-28817dec-1af1-11e8-8e0b-cd1c5154c843.JPG)

## Implementing a SQL Query

The biggest dataset on Kaggle is 3 terabytes. Since the monthly quota for BigQuery queries is 5 terabytes, we can easily run a couple of queries. One way to help avoid this is to estimate how big your query will be before you actually execute it. You can do this with the `BigQueryHelper.estimate_query_size()` method.

        #this query looks in the full table in the hacker_news  
        >> query = """SELECT score
                      FROM `bigquery-public-data.hacker_news.full`
                      WHERE type = "job" """
        
        # check how big this query will be
        hacker_news.estimate_query_size(query)
        
The output of the above query is 0.1524811713024974 which is almost equals to 150 MB. Now we have two methods available to run the query:
* `BigQueryHelper.query_to_pandas(query)`: This method takes a query and returns a Pandas dataframe.
* `BigQueryHelper.query_to_pandas_safe(query, max_gb_scanned=1)`: This method takes a query and returns a Pandas dataframe only if the       size of the query is less than the upperSizeLimit (1 gigabyte by default).
      
      # check out the scores of job postings (if the 
      # query is smaller than 1 gig)
      >> job_post_scores = hacker_news.query_to_pandas_safe(query)

Since this has returned a dataframe, we can work with it as we would any other dataframe. For example, we can get the mean of the column:

      # average score for job posts
      >> job_post_scores.score.mean()  

The output will be 2.1458. Lastly we can also save our new dataframe in a .csv fileto use later on in our kernel. The below code will create job_post_scores.csv file.

      # save our dataframe as a .csv 
      >> job_post_scores.to_csv("job_post_scores.csv")
      
We can perform various commands for the bigquery datasets. You can check all the [Kernels](https://www.kaggle.com/nitsbat/kernels) i made using BigQuery in various datasets. The repository contains all the python codes i used to extract maximum information from Big datasets.  
