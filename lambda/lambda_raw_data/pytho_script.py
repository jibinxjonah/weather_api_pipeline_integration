import pandas as pd
from datetime import datetime
import boto3
import requests
import json
import time
import os # Import the os module for environment variables

# --- Global Scope: Client Initialization ---
# Best practice to initialize clients outside the handler to improve performance
try:
    s3_client = boto3.client('s3')
except Exception as e:
    print(f"Error initializing S3 client: {e}")
    s3_client = None


# --- Helper Function for API Call (Can be left in global scope) ---
def get_weather_data(api_key, city_list):
    """
    Fetches raw weather data for a list of cities.
    """
    base_url = "http://api.weatherapi.com/v1"
    endpoint = "/current.json"
    
    all_weather_data = []
    
    for city in city_list:
        params = {
            "key": api_key,
            "q": city
        }
        
        try:
            print(f"Fetching data for {city}...")
            response = requests.get(base_url + endpoint, params=params)
            response.raise_for_status()
            
            raw_data = response.json()
            all_weather_data.append(raw_data)
            time.sleep(1) 
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city}: {e}")
            continue
            
    return all_weather_data


# --- The Lambda Handler: This is the entry point for your function ---
def lambda_handler(event, context):
    """
    The main function that is executed by AWS Lambda.
    """
    # --- Code to be executed on each invocation ---
    
    # It's a best practice to get sensitive information from environment variables
    # api_key = os.environ.get("WEATHER_API_KEY")
    api_key = "a63c813cc1924ab5a7e65942251309" # Still hardcoded for now, but a good place to change
    
    # List of at least 30 major cities from around the world
    cities = ['Mumbai', 'New Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Ahmedabad', 'Pune']
    
    weather_data_list = get_weather_data(api_key, cities)
    
    if not weather_data_list:
        print("Failed to retrieve any weather data. Exiting.")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to retrieve weather data')
        }
    
    # The data is already in raw format (list of dictionaries)
    # To store it in a single-line string, use json.dumps()
    raw_json_output = json.dumps(weather_data_list, indent=None)
    
    print("\n--- Raw Weather Data Output ---")
    print(raw_json_output)
    
    # --- Dump To S3 ---
    # These variables must be defined inside the handler
    # This ensures they are created with each invocation
    bucket_name = 'jibin.spotify.dump'
    folder_name = 'raw_json'
    file_name = f"output_{datetime.now().strftime('%Y-%m-%d')}.json"
    s3_file_key = f"{folder_name}/{file_name}"
    
    try:
        if s3_client:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_file_key, 
                Body=raw_json_output,
                ContentType='application/json'
            )
            print(f'Successfully dumped JSON to S3: s3://{bucket_name}/{s3_file_key}')
        else:
            print("S3 client not initialized. Cannot dump file.")
            
    except Exception as e:
        print(f"Error dumping JSON to S3: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error dumping JSON to S3: {e}')
        }
        
    # --- Lambda function must return a response ---
    return {
        'statusCode': 200,
        'body': json.dumps('JSON dumped to S3 successfully!')
    }


# --- Optional: Local Test Block ---
# This block is for local testing and will not be executed by AWS Lambda
if __name__ == "__main__":
    print("Running in local test mode...")
    # Simulate a Lambda event and context
    lambda_handler({}, {})