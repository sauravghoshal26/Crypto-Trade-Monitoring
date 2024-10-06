# for multiple crypto monitoring
from kafka import KafkaProducer
import json
import requests
import time
import logging
from datetime import datetime, timezone
from decimal import Decimal  # Import Decimal for handling float types

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

# List of cryptocurrencies to track
crypto_symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "LTCUSDT"]

def fetch_crypto_data(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching crypto data for {symbol}: {e}")
        return None

def kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        retries=5  # Retry sending in case of errors
    )
    
    try:
        while True:
            for symbol in crypto_symbols:
                crypto_data = fetch_crypto_data(symbol)
                if crypto_data:
                    # Add the current timestamp to the data using UTC
                    crypto_data['timestamp'] = datetime.now(timezone.utc).isoformat()  # Use UTC now
                    # Ensure price is converted to Decimal and sent as string
                    crypto_data['price'] = float(crypto_data['price'])  
                    producer.send('crypto_trades', value=crypto_data)
                    logging.info(f'Sent data: {crypto_data}')  # Log the sent data
            time.sleep(10)  # Fetch every 10 seconds to avoid API limits
    except KeyboardInterrupt:
        logging.info("Shutting down producer...")
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    kafka_producer()






# for specific crypto monitoring

# from kafka import KafkaProducer
# import json
# import requests
# import time
# import logging
# from datetime import datetime, timezone
# from decimal import Decimal  # Import Decimal for handling float types

# # Set up logging for better error tracking
# logging.basicConfig(level=logging.INFO)

# def fetch_crypto_data(symbol="BTCUSDT"):
#     url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()  # Raise an exception for bad status codes
#         return json.loads(response.text)
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error fetching crypto data: {e}")
#         return None

# def kafka_producer():
#     producer = KafkaProducer(
#         bootstrap_servers=['localhost:9092'],
#         value_serializer=lambda x: json.dumps(x).encode('utf-8'),
#         retries=5  # Retry sending in case of errors
#     )
    
#     try:
#         while True:
#             crypto_data = fetch_crypto_data()
#             if crypto_data:
#                 # Add the current timestamp to the data using UTC
#                 crypto_data['timestamp'] = datetime.now(timezone.utc).isoformat()  # Use UTC now
#                 # Ensure price is converted to Decimal and sent as string
#                 crypto_data['price'] = float(crypto_data['price'])  
#                 producer.send('crypto_trades', value=crypto_data)
#                 logging.info(f'Sent data: {crypto_data}')  # Log the sent data
#             time.sleep(2)
#     except KeyboardInterrupt:
#         logging.info("Shutting down producer...")
#     finally:
#         producer.flush()
#         producer.close()

# if __name__ == "__main__":
#     kafka_producer()
