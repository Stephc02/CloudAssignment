import os
from flask import Flask, jsonify, render_template
import random
from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Initialize Storage client
storage_client = storage.Client()
bucket_name = os.environ.get('CLOUD_STORAGE_BUCKET', 'random-numbers1')
bucket = storage_client.get_bucket(bucket_name)

@app.route('/')
def home():
    return render_template('index.html')

def generate_random_numbers(instance_name):
    numbers = []
    for _ in range(1000):
        random_number = random.randint(0, 100000)
        numbers.append(random_number)
    
    # Store the numbers in cloud storage
    blob = bucket.blob(f'random_numbers/{instance_name}.txt')
    blob.upload_from_string(','.join(map(str, numbers)))

@app.route('/generate_and_store', methods=['GET'])
def generate_and_store():
    # Get the current GAE instance name
    gae_instance = os.environ.get('GAE_INSTANCE', 'Instance Not Found')

    with ThreadPoolExecutor() as executor:
        for i in range(10):
            instance_name = f'{gae_instance}_instance_{i}'
            executor.submit(generate_random_numbers, instance_name)

    return 'Random numbers generated and stored successfully.'

@app.route('/get_results', methods=['GET'])
def get_results():
    numbers = []
    blobs = bucket.list_blobs(prefix='random_numbers/')
    
    for blob in blobs:
        data = blob.download_as_string().decode('utf-8')
        numbers.extend(map(int, data.split(',')))

    smallest_number = min(numbers)
    largest_number = max(numbers)

    return jsonify({'smallest_number': smallest_number, 'largest_number': largest_number})

if __name__ == '__main__':
    app.run(debug=True)
