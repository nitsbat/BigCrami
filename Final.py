# We have choosen the Hacker_news dataset.

import bq_helper
hacker = bq_helper.BigQueryHelper(active_project = "bigquery-public-data", dataset_name = "hacker_news")

#List of tables Present in dataset Hacker_News

hacker.list_tables()

#  Counting the Authors who have commented more than 500 times

hacker.head('comments')
query = """    select author_name , total
               from  (select author as author_name,count(author) as total 
                from `bigquery-public-data.hacker_news.comments` group by author_name)
                where total > 500
                """
hacker.estimate_query_size(query)
pos = hacker.query_to_pandas_safe(query)
pos.head()

query1 = """    select count(DISTINCT author) 
                from `bigquery-public-data.hacker_news.comments` 
                where extract(YEAR from time_ts) = 2013 and ranking > 1
         """
hacker.estimate_query_size(query1)
hacker.query_to_pandas_safe(query1)

#We have now choosen the 'full' table of the hacker_news dataset.
#The below code will result into the comparison between the users who posted a story or a comment.

query = """ select type,count(id) from `bigquery-public-data.hacker_news.full`
            group by type
        """
hacker.estimate_query_size(query)
hacker.query_to_pandas_safe(query)

#The below query will return the number of times a particular username has done some action where action consists of comment, comment_ranking, poll, story, job and pollopt.

query = """         select `by`,type,count(`by`) as total 
                    from `bigquery-public-data.hacker_news.full`
                    group by `by`, type
                    order by total DESC
        """
hacker.estimate_query_size(query)
k = hacker.query_to_pandas_safe(query)
k.head()

#The above result clearly shows that some anonymous has posted the maximum number of comments and stories.
#The below query shows the number of people who commented and posted stories maximum number of times and the result is as we have already seen the user is Anonymous

query = """         WITH new_tab as
                    (
                        select `by` as author_name,type,count(`by`) as total 
                        from `bigquery-public-data.hacker_news.full`
                        group by `by`, type
                    )
                    select author_name,type,total from new_tab
                    where total = (
                    select max(total) from new_tab where type = 'comment'
                    ) or total = (
                    select max(total) from new_tab where type = 'story'
                    )
        """

hacker.estimate_query_size(query)
hacker.query_to_pandas_safe(query)

#Now we will extract the assign each username its real name that is author name from the comments and stories table.
#The assignment will be done for the valid usernames only. i.e Inner Join

query = """         WITH new_tab as
                    (
                        select `by` as author_name,type,count(`by`) as total 
                        from `bigquery-public-data.hacker_news.full`
                        group by `by`, type
                    )
                    select a.author, b.type, b.total
                    from `bigquery-public-data.hacker_news.comments` as a 
                    join new_tab as b
                    on a.author = b.author_name
        """

hacker.estimate_query_size(query)
res = hacker.query_to_pandas_safe(query,max_gb_scanned=1)
res.head()

# The output will reveal that only the persons with type "job" have posted stories and commented the maximum times