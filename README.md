# weather_api_pipeline_integration
Event-driven ELT architecture on AWS and Snowflake to capture hourly weather insights


Ingestion & Trigger (λ + S3): EventBridge triggers an AWS Lambda function hourly to fetch data from the Weather API, clean it, and drop the file into an S3 bucket (the data lake landing zone).
Notification (SQS): An S3 event triggers a second Lambda, which sends a notification message (containing the S3 path) to an SQS queue. This ensures reliable hand-off and decoupling.
Near Real-Time Loading (SnowPipe): Snowflake's SnowPipe is configured to monitor the SQS queue. As soon as a message arrives, SnowPipe automatically and continuously loads the new weather file from S3 into a staging table in Snowflake. No manual COPY statements needed!
Analytics & Visualization: The structured data in Snowflake is then connected to Power BI for automated dashboards, enabling instant trend analysis and insights.
