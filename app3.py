import os
from flask import Flask
import random
from google.cloud import storage

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\ANNE CREMONA\Downloads\gifted-pulsar-422809-q0-b4d9cc90c98c.json"

# Get instance number from environment variable 
instance_number = os.environ.get('GAE_INSTANCE')

app = Flask(__name__)

# Initialize Storage client
storage_client = storage.Client()

bucket_name = 'random-numbers1'
bucket = storage_client.get_bucket(bucket_name)

@app.route('/')
def home():
    return 'Welcome to the Random Number Generator App!'

@app.route('/generate_and_store', methods=['GET'])
def generate_and_store():
    for _ in range(1000):
        # Generate a random number
        random_number = random.randint(1, 1000)

        # Create a blob object to store the random number
        blob = bucket.blob(f'random_number_{random_number}.txt')

        # Upload the random number to the storage bucket
        blob.upload_from_string(str(random_number))

    return '1000 random numbers have been generated and stored in the storage bucket.'

@app.route('/get_results', methods=['GET'])
def get_results():
    blobs = bucket.list_blobs()
    numbers = [int(blob.download_as_string()) for blob in blobs]
    
    smallest_number = min(numbers)
    largest_number = max(numbers)
    
    smallest_instance = [blob.name for blob in blobs if int(blob.download_as_string()) == smallest_number][0]
    largest_instance = [blob.name for blob in blobs if int(blob.download_as_string()) == largest_number][0]
    
    return f'Smallest Number: {smallest_number}, Largest Number: {largest_number}, Instance Name of Smallest Number: {smallest_instance}, Instance Name of Largest Number: {largest_instance}'


if __name__ == '__main__':
    app.run(debug=True)