from kafka import KafkaConsumer
import json
import logging
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'CryptoTrades'  # Name of your DynamoDB table
table = dynamodb.Table(table_name)

# Initialize SNS client
sns_client = boto3.client('sns')
alert_topic_arn = 'arn:aws:sns:us-east-1:465878727851:CryptoAlert'  # Replace with your SNS Topic ARN

# Define alert thresholds for each crypto
ALERT_THRESHOLDS = {
    'BTCUSDT': Decimal('30000'),
    'ETHUSDT': Decimal('2000'),
    'XRPUSDT': Decimal('0.50'),
    'BNBUSDT': Decimal('250'),
    'LTCUSDT': Decimal('100')
}

# Function to send alert via SNS
def send_alert(symbol, price):
    message = f"Alert! The price of {symbol} has dropped below your threshold: ${price}."
    try:
        sns_client.publish(
            TopicArn=alert_topic_arn,
            Message=message,
            Subject=f"Price Alert for {symbol}"
        )
        logging.info(f"Alert sent for {symbol} at price ${price}")
    except ClientError as e:
        logging.error(f"Failed to send alert: {e}")

# Function to store the trade data in DynamoDB
def store_trade(data):
    try:
        # Ensure price is converted to Decimal before storing
        data['price'] = Decimal(str(data['price']))  # Convert string price to Decimal
        table.put_item(Item=data)
        logging.info(f"Stored trade: {data}")
    except ClientError as e:
        logging.error(f"Failed to store trade: {e}")

# Kafka consumer function
def kafka_consumer():
    consumer = KafkaConsumer(
        'crypto_trades',  # Topic to consume from
        bootstrap_servers=['localhost:9092'],  # Kafka broker address
        auto_offset_reset='earliest',  # Start from the earliest available message
        enable_auto_commit=True,  # Commit offsets automatically
        group_id='crypto-group',  # Consumer group ID
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON
    )

    logging.info("Consumer started. Listening for messages...")

    try:
        for message in consumer:
            price_data = message.value
            logging.info(f"Received data: {price_data}")

            # Store the trade in the database
            store_trade(price_data)

            # Check for alert condition
            symbol = price_data['symbol']
            price_as_decimal = Decimal(price_data['price'])  # Convert price from string to Decimal
            logging.info(f"Checking price for alert: {price_as_decimal}")

            if symbol in ALERT_THRESHOLDS and price_as_decimal < ALERT_THRESHOLDS[symbol]:
                send_alert(symbol, price_as_decimal)
    except Exception as e:
        logging.error(f"Error in Kafka consumer: {e}")
    finally:
        consumer.close()  # Ensure consumer is properly closed when stopping
        logging.info("Kafka consumer has been shut down.")

if __name__ == "__main__":
    try:
        kafka_consumer()
    except KeyboardInterrupt:
        logging.info("Shutting down consumer...")


# if you want to store the data in a DynamoDB table and send an SNS alert for single crypto monitored, you can modify the consumer code as follows:

# from kafka import KafkaConsumer
# import json
# import logging
# import boto3
# from botocore.exceptions import ClientError
# from decimal import Decimal

# # Set up logging for better error tracking
# logging.basicConfig(level=logging.INFO)

# # Initialize DynamoDB client
# dynamodb = boto3.resource('dynamodb')
# table_name = 'CryptoTrades'  # Name of your DynamoDB table
# table = dynamodb.Table(table_name)

# # Initialize SNS client
# sns_client = boto3.client('sns')
# alert_topic_arn = 'arn:aws:sns:us-east-1:465878727851:CryptoAlert'  # Replace with your SNS Topic ARN

# # Define alert threshold
# ALERT_THRESHOLD = Decimal('30000')  # Set your desired threshold here

# # Function to send alert via SNS
# def send_alert(symbol, price):
#     message = f"Alert! The price of {symbol} has dropped below your threshold: ${price}."
#     try:
#         response = sns_client.publish(
#             TopicArn=alert_topic_arn,
#             Message=message,
#             Subject=f"Price Alert for {symbol}"
#         )
#         logging.info(f"Alert sent for {symbol} at price ${price}")
#     except ClientError as e:
#         logging.error(f"Failed to send alert: {e}")

# # Function to store the trade data in DynamoDB
# def store_trade(data):
#     try:
#         # Ensure price is converted to Decimal before storing
#         data['price'] = Decimal(str(data['price']))  # Convert string price to Decimal
#         table.put_item(Item=data)
#         logging.info(f"Stored trade: {data}")
#     except ClientError as e:
#         logging.error(f"Failed to store trade: {e}")

# # Kafka consumer function
# def kafka_consumer():
#     consumer = KafkaConsumer(
#         'crypto_trades',  # Topic to consume from
#         bootstrap_servers=['localhost:9092'],  # Kafka broker address
#         auto_offset_reset='earliest',  # Start from the earliest available message
#         enable_auto_commit=True,  # Commit offsets automatically
#         group_id='crypto-group',  # Consumer group ID
#         value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON
#     )

#     logging.info("Consumer started. Listening for messages...")

#     try:
#         for message in consumer:
#             price_data = message.value
#             logging.info(f"Received data: {price_data}")

#             # Store the trade in the database
#             store_trade(price_data)

#             # Check for alert condition
#             if price_data['symbol'] == 'BTCUSDT':
#                 price_as_decimal = Decimal(price_data['price'])  # Convert price from string to Decimal
#                 logging.info(f"Checking price for alert: {price_as_decimal}")
#                 if price_as_decimal < ALERT_THRESHOLD:
#                     send_alert(price_data['symbol'], price_as_decimal)
#     except Exception as e:
#         logging.error(f"Error in Kafka consumer: {e}")
#     finally:
#         consumer.close()  # Ensure consumer is properly closed when stopping
#         logging.info("Kafka consumer has been shut down.")

# if __name__ == "__main__":
#     try:
#         kafka_consumer()
#     except KeyboardInterrupt:
#         logging.info("Shutting down consumer...")



#If you want to store the data in a SQLite database and send an email alert, you can modify the consumer code as follows:

# from kafka import KafkaConsumer
# import json
# import logging
# import sqlite3
# import smtplib
# from email.mime.text import MIMEText

# # Set up logging for better error tracking
# logging.basicConfig(level=logging.INFO)

# # Create or connect to a SQLite database
# conn = sqlite3.connect('crypto_trades.db')
# cursor = conn.cursor()

# # Create a table for storing trades if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS trades (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         symbol TEXT,
#         price REAL,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
# ''')
# conn.commit()

# # Define alert threshold
# ALERT_THRESHOLD = 30000  # Set your desired threshold here

# # Function to send alert email
# def send_alert(symbol, price):
#     msg = MIMEText(f"Alert! The price of {symbol} has dropped below your threshold: ${price}.")
#     msg['Subject'] = f"Price Alert for {symbol}"
#     msg['From'] = 'your_email@example.com'  # Replace with your email
#     msg['To'] = 'recipient@example.com'  # Replace with the recipient's email

#     # Send the email (using a simple SMTP server)
#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login('your_email@example.com', 'your_email_password')  # Replace with your email and password
#             server.send_message(msg)
#         logging.info(f"Alert sent for {symbol} at price ${price}")
#     except Exception as e:
#         logging.error(f"Failed to send alert: {e}")

# def store_trade(data):
#     cursor.execute('''
#         INSERT INTO trades (symbol, price) VALUES (?, ?)
#     ''', (data['symbol'], data['price']))
#     conn.commit()

# def kafka_consumer():
#     consumer = KafkaConsumer(
#         'crypto_trades',  # Make sure this matches the topic in your producer
#         bootstrap_servers=['localhost:9092'],
#         auto_offset_reset='earliest',
#         enable_auto_commit=True,
#         group_id='crypto-group',
#         value_deserializer=lambda x: json.loads(x.decode('utf-8'))
#     )

#     logging.info("Consumer started. Listening for messages...")

#     for message in consumer:
#         price_data = message.value
#         logging.info(f"Received data: {price_data}")

#         # Store the trade in the database
#         store_trade(price_data)

#         # Check for alert condition
#         if price_data['symbol'] == 'BTCUSDT' and float(price_data['price']) < ALERT_THRESHOLD:
#             send_alert(price_data['symbol'], price_data['price'])

# if __name__ == "__main__":
#     try:
#         kafka_consumer()
#     except KeyboardInterrupt:
#         logging.info("Shutting down consumer...")
#     finally:
#         conn.close()

