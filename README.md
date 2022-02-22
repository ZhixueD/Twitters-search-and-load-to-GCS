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



