"""Example Airflow DAG that search and download most recent 20 twitters, update and load to google cloud storage every 5 min
This DAG relies on three Airflow variables
* project_id - Google Cloud Project ID to use for the Cloud Dataflow cluster.
* gce_zone - Google Compute Engine zone where Cloud Dataflow cluster should be
  created.
* gce_region - Google Compute Engine region where Cloud Dataflow cluster should be
  created.
"""
import datetime
from airflow import models
from airflow.operators.python_operator import PythonOperator
#from airflow.utils.dates import days_ago
import datetime

import tweepy
import pandas as pd
import json
#from os import environ
#from google.cloud import storage

api_key= ####
api_key_secret=####
access_token=####
access_token_secret=####
bearer_token=####

# Define the python function for PythonOperator

def searchTweets(query):

    #Connect API
    
    client = tweepy.Client(bearer_token=bearer_token,
                          consumer_key=api_key,
                          consumer_secret=api_key_secret,
                          access_token=access_token,
                          access_token_secret=access_token_secret)
    
    #Search recent twitters
    
    tweets=client.search_recent_tweets(query=query, max_results=20,tweet_fields=['id','text','created_at'])
    
#     tweets=client.search_recent_tweets(query=query, tweets_fields=['id','text','created_at'],
#                                       media_fields=['preview_image_url'], expansions='attachments.media_keys',
#                                       max_results=10)
    tweet_data = tweets.data
    result = []
    
    #save file into result list
    if not tweet_data is None and len(tweet_data)>0:
        for tweet in tweet_data:
            obj = {}
            obj['id'] = tweet.id
            obj['text'] = tweet.text
            obj['created_at']=tweet.created_at
            result.append(obj)
    else:
        return ''
    
    #change result format to dataframe
    
    column=['id','text','time']
    df = pd.DataFrame(result)
    
    #Save dataframe to google cloud storage
    df.to_csv('gs://brant-twitter-search/twitter.csv')



bucket_path = models.Variable.get("bucket_path")
project_id = models.Variable.get("project_id")
gce_region = models.Variable.get("gce_region")


default_args = {
    # Tell airflow to start 5 mins ago, so that it runs as soon as you upload it
    "start_date": datetime.datetime.now()-datetime.timedelta(minutes=5),
    "dataflow_default_options": {
        "project": project_id,
        # Set to your region
        "region": gce_region,
        # Set to your zone
    },
}

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.


with models.DAG(
    # The id you will see in the DAG airflow page
    "twitter_dag2",
    default_args=default_args,
    # The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(minutes=5),  # Override to match your needs
    ) as dag:

# define the task
    twitters_search_load = PythonOperator(
		task_id='twitters_search_load',
		python_callable = searchTweets,
                op_kwargs = {"query" : "sweden"},
		dag=dag)

twitters_search_load    
