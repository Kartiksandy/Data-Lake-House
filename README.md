## Building a Data Lakehouse with AWS: A Guide to Cost-Effective Data Engineering

 ![image](https://github.com/user-attachments/assets/c8538b3d-4ac2-4aac-949d-7d3b34c326b0)

# Introduction
In this project, we dive into how to leverage AWS services to build a robust data lakehouse using NYC yellow taxi data. This guide walks you through setting up an efficient AWS architecture that includes data storage, orchestration, and processing using S3, Lambda, and Glue Crawler. Our goal is to showcase a cost-effective and efficient approach to data engineering.

#System Architecture
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
![image](https://github.com/user-attachments/assets/623e3b89-07de-43fc-a4f6-1b5495a0baa9)

 
This screenshot shows the S3 bucket `lakehouse001` set up to trigger the Lambda function on the `s3:ObjectCreated:*` event.

AWS Athena Query Editor

 ![image](https://github.com/user-attachments/assets/b38a1d79-65fa-4f39-9f24-db12865400aa)

We query the data in AWS Athena to ensure that the Glue Crawler has updated the data catalog correctly.


AWS Glue Crawler

The Glue Crawler `taxi_crawl` is configured and ready to run, connected to the data source in S3.
 

![image](https://github.com/user-attachments/assets/c83eddcb-a88e-4819-9a08-d14f3ea444dc)



S3 Bucket Structure

 ![image](https://github.com/user-attachments/assets/ba5828c0-2a87-4d10-b090-cb63e70fc25e)

The S3 bucket `lakehouse001` contains the folders for the data input (`Data_Taxi`) and other relevant directories.

Lambda Function Code
![image](https://github.com/user-attachments/assets/c9a634fc-4942-4125-85de-b6f6e20da0eb)

 
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

## Realtime Streaming with Data Lakehouse

![image](https://github.com/user-attachments/assets/e30565a0-9029-4caf-a94b-b3f82cec420f)


The Realtime Lakehouse system is designed to ingest, store, and process real-time data from various sources. The system uses a combination of Confluent's Kafka, MinIO for object storage, and Spark for data processing. This documentation provides a detailed overview of the system's architecture, configuration, and components as depicted in the provided screenshots.
Prerequisites

•  Programming Languages: Python, Java
•  Big Data Technologies: Apache Kafka, Apache Spark, Apache Flink
•  Cloud and Storage: MinIO, AWS S3
•  Data Processing: Pandas
•  Containerization: Docker, Docker Compose
•  Automation and Scripting: Bash, Shell Scripting

Objective

To set up a Kafka Broker in KRaft mode, integrate it with a MinIO S3 bucket for data ingestion, and create a Python script to ingest data from MinIO to Kafka and consume it.






Step 1: Setting Up Kafka Broker in KRaft Mode
Docker Compose Configuration

Created a Docker Compose file to configure Kafka brokers in KRaft mode, ensuring high availability and fault tolerance.
The docker-compose.yml file orchestrates the deployment of various services required for the Realtime Lakehouse system. Below are the key components configured in the docker-compose.yml file:
•  Define Services: We define two services for our Kafka brokers (broker1 and broker2) using the latest Confluent Kafka image.
•  Environment Variables: Set environment variables to configure the brokers. This includes enabling KRaft mode, setting listener configurations, and defining the node IDs and log directories.
•  Volumes: Mount the local directory to the Kafka data directory inside the container to persist Kafka logs.
![image](https://github.com/user-attachments/assets/7a856bee-d1e1-4b7b-9cde-55f7e9722c69)

 

2. Docker Dashboard
The Docker dashboard provides an overview of the running containers, their status, resource usage, and ports. Key observations include:
•	Realtime Lakehouse container is running.
•	Schema Registry, Control Center, Spark Worker, MinIO containers are also running.
•	The Control Center is running on port 9021.
•	The Schema Registry is running on port 8081.

 ![image](https://github.com/user-attachments/assets/329dd7a0-8600-41b5-bbda-33254e9bbcb2)

3. Confluent Control Center
The Confluent Control Center provides a graphical interface to monitor and manage the Kafka cluster. Key sections include:

 
![image](https://github.com/user-attachments/assets/05f416fe-6256-4692-b1f9-0f06eafae890)


4. Producer Script
The producer script is responsible for connecting to the MinIO client and ingesting data into the Kafka topic.
Python Script for Data Ingestion
Created a Python script to read data from MinIO and produce it to Kafka.
1.	MinIO Configuration: Initialize the MinIO client with the appropriate access credentials and endpoint.
2.	Kafka Producer Configuration: Set up the Kafka producer with the necessary configuration, including the bootstrap servers and client ID.
3.	Data Ingestion Function: Define a function to read data from MinIO, process it using Pandas, and produce each record to Kafka.

 
![image](https://github.com/user-attachments/assets/03d0c35b-1665-480a-bfc9-bd6503b4cbf1)


5. MinIO Object Browser
The MinIO Object Browser provides an interface to manage and view the objects stored in the MinIO buckets.
•  Define MinIO Service: Add a service definition for MinIO, specifying the image, container name, environment variables for access credentials, and the command to start the MinIO server.
•  Ports and Volumes: Map the necessary ports (9000 for the MinIO web interface and 9001 for the console) and mount a local directory to persist MinIO data.
 
![image](https://github.com/user-attachments/assets/ba69b528-b73e-4185-afd8-e5b856d4410c)

6. Kafka Topics
The Kafka topics are managed through the Confluent Control Center. Key topic configurations include:
•	nyc_trip_records:
o	Messages: No new messages
o	Schema and Configuration settings are accessible

 

![image](https://github.com/user-attachments/assets/72be5493-fcb4-47f2-8ff5-ab5b38262afa)


![image](https://github.com/user-attachments/assets/634bf0c7-ee50-4b30-b126-4c1140f8e769)

 




 Data Flow
1.	Data Ingestion: Data is ingested from various sources and stored in the MinIO buckets.
2.	Processing: The producer script reads data from the MinIO buckets and publishes it to the Kafka topic nyc_trip_records.
3.	Monitoring: The Confluent Control Center is used to monitor the Kafka brokers, topics, and the overall data flow.
Conclusion
The Realtime Lakehouse system is a robust setup for real-time data processing and storage. The combination of Docker, Kafka, MinIO, and Spark provides a scalable and efficient architecture. The provided screenshots offer a clear view of the system's configuration and operation.

Conclusion
The Realtime Lakehouse system is a robust setup for real-time data processing and storage. The combination of Docker, Kafka, MinIO, and Spark provides a scalable and efficient architecture. The provided screenshots offer a clear view of the system's configuration and operation.



