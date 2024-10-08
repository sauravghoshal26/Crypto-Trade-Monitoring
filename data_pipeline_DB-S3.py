import boto3
import csv
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Initialize DynamoDB and S3 clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# DynamoDB table name
table_name = 'CryptoTrades'
table = dynamodb.Table(table_name)

# Fetch all items from the DynamoDB table with pagination
items = []
try:
    logging.info("Fetching data from DynamoDB table...")
    response = table.scan()
    items.extend(response['Items'])

    # Handle pagination if necessary
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    logging.info(f"Fetched {len(items)} items from DynamoDB.")
except Exception as e:
    logging.error(f"Error fetching data from DynamoDB: {e}")

# Check if items are fetched before writing to CSV
if items:
    # Create a CSV file in memory
    csv_file = 'crypto_trades.csv'
    try:
        logging.info("Writing data to CSV file...")
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['symbol', 'price', 'timestamp'])
            writer.writeheader()
            writer.writerows(items)
        logging.info(f"Data written to {csv_file}.")
    except Exception as e:
        logging.error(f"Error writing data to CSV: {e}")

    # Upload the CSV file to S3
    try:
        logging.info("Uploading CSV to S3...")
        s3.upload_file(csv_file, 'crypto-trade-monitoring', 'crypto_trades.csv')
        logging.info("Data exported successfully to S3!")
    except Exception as e:
        logging.error(f"Error uploading to S3: {e}")
else:
    logging.info("No data found in the DynamoDB table.")