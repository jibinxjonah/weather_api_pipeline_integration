# weather_api_pipeline_integration
### Project Overview
- This project implements a fully automated, serverless, event-driven data pipeline to collect hourly weather data, process it in the cloud, load it into a cloud data warehouse, and visualize the insights. It leverages a modern Extract, Load, Transform (ELT) architecture using AWS services for orchestration and Snowflake for analytical storage.
----

### Key Objectives:
1. Automated Ingestion: Fetch and process weather data on a reliable, hourly schedule.
2. Scalability & Durability: Utilize serverless and managed services (Lambda, SQS, S3) for high availability.
3. Near Real-Time Loading: Implement continuous data loading into the data warehouse using SnowPipe.
4. Business Intelligence: Connect the structured data to Power BI for dynamic reporting and analysis.
### Architecture Diagram
![Architecture](https://github.com/jibinxjonah/weather_api_pipeline_integration/blob/master/portfolio_project.png)
### Technology Stack
CategoryService/ToolPurposeData SourceWeather APIProvides the raw hourly weather data.Scheduling/EventsAWS EventBridgeTriggers the ingestion process on an hourly cron schedule.ProcessingAWS Lambda (×2)Two serverless functions for initial data fetching/cleansing and SQS notification generation.Data LakeAWS S3Highly durable storage for landing and staging the raw/processed weather files.Messaging/QueueAmazon SQSDecouples the S3 file creation from the Snowflake loading process.Data WarehouseSnowflakeScalable, analytical data platform for storing and querying the data.Continuous LoadingSnowflake SnowPipeAutomates the continuous, event-driven loading of files from S3 (via SQS) into Snowflake tables.VisualizationPower BIConnects to Snowflake for creating dashboards and deriving business insights.

### Pipeline Data Flow (Step-by-Step)
1. Event Trigger: EventBridge executes an hourly rule, triggering the first AWS Lambda function.
2. Data Fetch & Store: The Lambda calls the Weather API, processes the resulting data (e.g., converts to JSONL or CSV), and writes the file to the S3 Landing Bucket.
3. Notification: The S3 upload triggers a second AWS Lambda. This Lambda's job is to extract the file metadata (key/path) and send a reliable message to the Amazon SQS queue.
4. SnowPipe Integration: Snowflake SnowPipe is configured to monitor the SQS queue.
5. Data Load: When a new message is received, SnowPipe automatically pulls the corresponding file from the S3 bucket and loads the data into the designated table within Snowflake.
6. Analysis: Power BI connects directly to the Snowflake table, enabling analysts to build dashboards for tracking weather trends and generating actionable insights.
Repository Setup
### This repository contains the necessary code and configuration templates to deploy and manage the pipeline components.

### Deployment
1. AWS Setup: Deploy the core AWS infrastructure (Lambda, S3, SQS, EventBridge) using the Terraform configurations in the terraform/ directory.
2. Snowflake Setup: Configure the Snowflake database, external stage (pointing to S3), and the SnowPipe object using the provided DDL and Terraform. Ensure the SnowPipe service principal has the necessary IAM permissions to read from the S3 bucket.
3. API Key: Update the environment variables in the Lambda configuration with your specific Weather API key.
4. Insights & Visualization
   
-The final stage allows users to leverage the structured data in Snowflake via Power BI. Example visualizations include:
1. Hourly temperature and humidity trends.
2. Historical comparison of weather conditions.
3. Mapping data points for geographic analysis.
