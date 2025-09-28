import pandas as pd
import json
import boto3
import urllib.parse
from datetime import datetime
from io import StringIO # Import StringIO for in-memory CSV conversion

# --- Global Scope: Client Initialization ---
# This client is initialized once for all function invocations
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    The main function that is executed by AWS Lambda.
    It is triggered by an S3 PutObject event.
    """
    try:
        # --- 1. Get S3 bucket and key from the event payload ---
        # The S3 event trigger provides the bucket and key of the new file
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        print(f"Processing file: {s3_file_key} from bucket: {bucket_name}")
        
        # --- 2. Load the JSON from S3 ---
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_file_key) 
        raw_json_output = response['Body'].read()
        raw_json_output_json = json.loads(raw_json_output)
        
        # --- 3. Process the data with Pandas ---
        flattened_data = pd.json_normalize(raw_json_output_json, sep='_')
        
        print(f"Data has been flattened. Shape: {flattened_data.shape}")
        
        # --- 4. Dump the processed data to S3 as a CSV ---
        # Convert the DataFrame to a CSV string in memory
        csv_buffer = StringIO()
        flattened_data.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()
        
        # Define the output bucket and file name
        processed_folder = 'processed_data'
        output_file_name = s3_file_key.replace('.json', '.csv') # Maintain the same file name, just change extension
        output_s3_key = f"{processed_folder}/{output_file_name}"

        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_s3_key, 
            Body=csv_string,
            ContentType='text/csv'
        )
        print(f'Successfully dumped processed data to S3: s3://{bucket_name}/{output_s3_key}')

        # --- 5. Delete the raw JSON file from S3 ---
        # It's good practice to delete the original after successful processing
        s3_client.delete_object(Bucket=bucket_name, Key=s3_file_key)
        print(f'Successfully deleted raw JSON file: {s3_file_key}')

        return {
            'statusCode': 200,
            'body': json.dumps('Data processed and dumped to S3, raw file deleted!')
        }
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {e}')
        }