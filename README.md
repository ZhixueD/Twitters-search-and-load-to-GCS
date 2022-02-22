# Twitters-search-and-load-to-GCS

## About this project

In this project, I create a work flow using Airflow,  using twitter API to search most 20 recent twitters contain 'sweden' and load as a csv file to google cloud storage, this work flow run every 5 mins, and update the most recent searching result.
This workflow is create in google cloud composer (Airflow).

## The project contains follow steps:
1. Enable API used in this project.
2. Create a Composer environment. 
3. Create a Cloud Storage bucket, named: brant-twitter-search
4. Setting Airflow variables in Airflow web UI
5. Copy the DAG python file to Cloud Storage Dag folder
6. Exploring DAG runs

## 1. Enable API used in this project

(1) Enable Kubernetes Engine API 

![Kuberne API](https://user-images.githubusercontent.com/98153604/151383877-9e9cfc88-220c-4435-bf44-0e571f1290f4.JPG)


(2) Enable Cloud Composer API

![composer API](https://user-images.githubusercontent.com/98153604/151384240-f0e80581-ce74-40b4-a7d8-2339e08fa4b5.JPG)


## 2. Create a Composer environment.
Click CREATE ENVIRONMENT and select Composer 1. Set the following for your environment:
    Name	highcpu
    Location	europe-central2
    Zone	europe-central2-a
    Machine type	n1-highcpu-4
    
 leave others as default
 
 After create
 
 ![high cpu](https://user-images.githubusercontent.com/98153604/155223170-61dfd2ca-aa4e-4709-9e53-6c1b63fac953.JPG)
 
 Go to Computer Engine, it shows:
 
 ![vm](https://user-images.githubusercontent.com/98153604/155223211-c733cb40-a31e-4bb5-a489-2526448fdd8a.JPG)
 
 Go to Google cloud storage, you will see a new bucket create:
 
 ![dag bucket](https://user-images.githubusercontent.com/98153604/155223274-d2d273d0-1448-4901-a36d-d8dc31e0a675.JPG)
  
## 3. Create a Cloud Storage bucket, named: brant-twitter-search
 
 The bucket location set to europe-north1 (Finland)
 
 ![gcs bucket](https://user-images.githubusercontent.com/98153604/155221871-c9ac8bf5-4dc9-4a1a-9d7e-cda466ee8de4.JPG)

## 4. Setting Airflow variables in Airflow web UI
 
Go back to Composer to check the status of your environment.

Once your environment has been created, click the name of the environment (highcpu) to see its details.

On the Environment details you'll see information such as the Airflow web interface URL, Kubernetes Engine cluster ID, and a link to the DAGs folder, which is stored in your bucket.

![envioron](https://user-images.githubusercontent.com/98153604/155223779-4af0dfe1-95ee-4c71-8c5c-fa5a448c7875.JPG)

Open Airflow web interface URL, setting Airflow variables. Select Admin > Variables from the Airflow menu bar, then Create.

![airflow5](https://user-images.githubusercontent.com/98153604/151392941-0a705cbf-f411-428c-aae4-b44f63bb9e2b.JPG)

## 5. Copy the DAG python file to Cloud Storage Dag folder

In step4, in the environment configration, we will find DAG folder path: 'gs://europe-central2-highcpu-abc29983-bucket/dags'
Here we just up load the Python Dag file twitter_airflow2.py in DAG folder.

![Dag folder](https://user-images.githubusercontent.com/98153604/155224620-0e3ef4d2-47b4-435c-944f-5494868a321e.JPG)

After this The airflow start to run the whole work flow.

The Dag file contant:

        """Example Airflow DAG that search and download most recent 20 twitters, update and load to google cloud storage every 5 min
        This DAG relies on three Airflow variables
        * project_id - Google Cloud Project ID to use for the Cloud Dataflow cluster.
        * gce_zone - Google Compute Engine zone where Cloud Dataflow cluster should be
          created.
        * gce_region - Google Compute Engine region where Cloud Dataflow cluster should be
          created.
        """
        import datetime
        #import os
        from airflow import models
        from airflow.operators.python_operator import PythonOperator
        #from airflow.utils.dates import days_ago
        import datetime

        import tweepy
        import pandas as pd
        import json
        #from os import environ
        #from google.cloud import storage

        api_key= ###
        api_key_secret= ###
        access_token= ###
        access_token_secret= ###
        bearer_token= ###


        def searchTweets(query):

            client = tweepy.Client(bearer_token=bearer_token,
                                  consumer_key=api_key,
                                  consumer_secret=api_key_secret,
                                  access_token=access_token,
                                  access_token_secret=access_token_secret)


            tweets=client.search_recent_tweets(query=query, max_results=20,tweet_fields=['id','text','created_at'])

        #     tweets=client.search_recent_tweets(query=query, tweets_fields=['id','text','created_at'],
        #                                       media_fields=['preview_image_url'], expansions='attachments.media_keys',
        #                                       max_results=10)
            tweet_data = tweets.data
            result = []

            if not tweet_data is None and len(tweet_data)>0:
                for tweet in tweet_data:
                    obj = {}
                    obj['id'] = tweet.id
                    obj['text'] = tweet.text
                    obj['created_at']=tweet.created_at
                    result.append(obj)
            else:
                return ''

            column=['id','text','time']
            df = pd.DataFrame(result)

            df.to_csv('gs://brant-twitter-search/twitter.csv')



        bucket_path = models.Variable.get("bucket_path")
        project_id = models.Variable.get("project_id")
        gce_region = models.Variable.get("gce_region")


        default_args = {
            # Tell airflow to start one day ago, so that it runs as soon as you upload it
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

            # define the first task


            twitters_search_load = PythonOperator(
                task_id='twitters_search_load',
                python_callable = searchTweets,
                op_kwargs = {"query" : "sweden"},
                dag=dag)

        twitters_search_load
        
## 6. Exploring DAG runs

Open Airflow web interface:

![dag1](https://user-images.githubusercontent.com/98153604/155225594-83463e1d-4390-4e2e-8480-3429476f28e8.JPG)

![dag2](https://user-images.githubusercontent.com/98153604/155225691-4b262229-5e3c-41e5-883b-458d33ccfb1a.JPG)

## 7. Check Google cloud storage

1 csv file twitter.csv has been generated

![csv1](https://user-images.githubusercontent.com/98153604/155226140-1b26a14f-61b9-4611-82f9-25e47f95337c.JPG)

![csv2](https://user-images.githubusercontent.com/98153604/155226170-c065376d-2351-4599-9c57-d0b55c3fa591.JPG)

![csv3](https://user-images.githubusercontent.com/98153604/155226890-5ba1bfe2-3b07-4ce9-9ba0-bb87ceda649d.JPG)




