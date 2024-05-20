from flask import Flask, render_template, redirect, url_for, jsonify
from generate_numbers import generate_random_numbers, generate_and_store_subset
from google.cloud import storage
import multiprocessing
import os

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\ANNE CREMONA\Downloads\gifted-pulsar-422809-q0-b4d9cc90c98c.json"

# Initialize Storage client
storage_client = storage.Client()

app = Flask(__name__)

# Connect to the bucket
bucket_name = 'random-numbers1'
bucket = storage_client.get_bucket(bucket_name)

@app.route('/submit', methods=['POST'])
def submit():
    # Generate and store random numbers in Google Cloud Storage
    generate_and_store_numbers()
   
    # Redirect to the route that displays the results
    return redirect(url_for('get_results'))

def generate_and_store_numbers():
    num_instances = 10
    num_numbers_per_instance = 1000
   
    with multiprocessing.Pool(processes=num_instances) as pool:
        pool.starmap(generate_and_store_subset, [(i, num_numbers_per_instance) for i in range(num_instances)])

@app.route('/get_results', methods=['GET'])
def get_results():
    # Retrieve the stored random numbers from Google Cloud Storage
    blobs = bucket.list_blobs()
    random_numbers = []
    for blob in blobs:
        random_numbers.append(int(blob.download_as_string()))
    
    # Calculate the smallest and largest numbers
    min_number = min(random_numbers)
    max_number = max(random_numbers)
    
    # Return the results as a JSON response
    return jsonify({'min_number': min_number, 'max_number': max_number})

if __name__ == '__main__':
    app.run(debug=True)