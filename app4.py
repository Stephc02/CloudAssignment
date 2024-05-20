import os
from flask import Flask, jsonify
import random
from google.cloud import storage

app = Flask(__name__)

# Initialize Storage client
storage_client = storage.Client()
bucket_name = os.environ.get('CLOUD_STORAGE_BUCKET', 'random-numbers1')
bucket = storage_client.get_bucket(bucket_name)

@app.route('/generate_and_store', methods=['GET'])
def generate_and_store():
    # Get the current GAE instance name
    gae_instance = os.environ.get('GAE_INSTANCE', 'Instance Not Found')

    for _ in range(10000):
        # Generate a random number between 0 and 100,000
        random_number = random.randint(0, 100000)
        
        # Create a blob object with the instance name to store the random number
        blob = bucket.blob(f'random_numbers/{gae_instance}/random_number_{random_number}.txt')
        blob.upload_from_string(str(random_number))
    
    return 'Random numbers generated and stored successfully.'

@app.route('/get_results', methods=['GET'])
def get_results():
    blobs = bucket.list_blobs(prefix=f'random_numbers/')
    
    numbers = []
    for blob in blobs:
        number = int(blob.download_as_string())
        instance = blob.name.split('/')[1]
        numbers.append({'number': number, 'instance': instance})
    
    smallest = min(numbers, key=lambda x: x['number'])
    largest = max(numbers, key=lambda x: x['number'])
    
    return jsonify({'smallest_number': smallest['number'], 'smallest_instance': smallest['instance'],
                    'largest_number': largest['number'], 'largest_instance': largest['instance']})

if __name__ == '__main__':
    app.run(debug=True)