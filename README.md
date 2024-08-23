Building a Data Lakehouse with AWS: A Guide to Cost-Effective Data Engineering

 

Introduction
In this project, we dive into how to leverage AWS services to build a robust data lakehouse using NYC yellow taxi data. This guide walks you through setting up an efficient AWS architecture that includes data storage, orchestration, and processing using S3, Lambda, and Glue Crawler. Our goal is to showcase a cost-effective and efficient approach to data engineering.

System Architecture
Data Input
- Sources: We use multiple data sources including Apache Airflow, Python scripts, Java applications, and direct file uploads.
- Storage: Raw data is stored in S3 buckets, referred to as Brun Storage.

AWS Glue Crawler
- Purpose: The Glue Crawler scans the S3 buckets to create a data catalog, making data easily searchable and queryable.
- Challenges: A notable challenge with Glue Crawlers is their minimum run time of 5 minutes and lack of event-driven triggers.

AWS Lambda Function
- Functionality: AWS Lambda functions listen for events in the S3 bucket and trigger the Glue Crawler. This helps in making the process event-driven and more efficient.

Modern System Architecture
- Data Input: Remains the same, utilizing multiple data sources.
- Storage: MinIO can be used as an alternative to some AWS services to reduce costs.
- Processing: Data is processed using Apache Spark and Apache Flink for real-time and batch processing, ensuring data integrity and efficiency.

Implementation on AWS

1. Setting Up S3 Buckets
   - We set up an S3 bucket named `lakehouse001` to store our raw data.

2. AWS Glue Crawler Configuration
   - We configure the Glue Crawler to scan the `lakehouse001` bucket and catalog the data into a database and tables.

3. AWS Lambda Function Configuration
   - We create a Lambda function (`taxidb_function`) that triggers the Glue Crawler based on S3 events.
   - Necessary permissions for S3 and Glue are granted to the Lambda function to ensure smooth operation.

4. Testing
   - We test the setup by uploading files to S3 and verifying that the Glue Crawler is triggered automatically by the Lambda function.

Data Source
For this project, we utilized the NYC yellow taxi trip data. This dataset contains comprehensive trip records including pickup and drop-off times, locations, distances, and fare amounts, making it an ideal choice for demonstrating the capabilities of a data lakehouse.

Lambda Trigger Configuration
 
This screenshot shows the S3 bucket `lakehouse001` set up to trigger the Lambda function on the `s3:ObjectCreated:*` event.

AWS Athena Query Editor

 
We query the data in AWS Athena to ensure that the Glue Crawler has updated the data catalog correctly.


AWS Glue Crawler

The Glue Crawler `taxi_crawl` is configured and ready to run, connected to the data source in S3.
 




S3 Bucket Structure
 
The S3 bucket `lakehouse001` contains the folders for the data input (`Data_Taxi`) and other relevant directories.

Lambda Function Code
 
The Lambda function code initializes AWS clients and triggers the Glue Crawler based on S3 events.

## Code
-----------------------------------------------------------------------------------------
import json
import boto3

# initializing AWS client
glue = boto3.client('glue')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    # Debugging statement to print the event structure
    print("Received event: " + json.dumps(event, indent=2))
    
    # get bucket name and file key
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        
        # specify the glue crawler name
        crawler_name = 'taxi_crawl'
        
        # start the glue crawler
        response = glue.start_crawler(Name=crawler_name)
        print(f'Glue crawler {crawler_name} started successfully')
    except KeyError as e:
        print(f'KeyError: {e}')
        raise e
    except Exception as e:
        print(f'Error starting Glue crawler {crawler_name}: {e}')
        raise e
--------------------------------------------------------------------------------------------
Conclusion
This project demonstrates how to build a cost-effective data lakehouse using AWS services. By setting up event-driven data processing with S3, Lambda, and Glue Crawler, we ensure efficient data storage, orchestration, and processing. This architecture is not only efficient but also scalable, making it suitable for large-scale data engineering projects.

For detailed instructions and code, refer to the complete documentation and video tutorial. Feel free to explore the dataset and implementation details in the attached resources. Your feedback and suggestions are welcome to improve this project further.


![image](https://github.com/user-attachments/assets/c8538b3d-4ac2-4aac-949d-7d3b34c326b0)
