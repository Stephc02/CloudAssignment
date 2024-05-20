import random
from google.cloud import storage

storage_client = storage.Client()
bucket_name = 'random-numbers1'

def generate_random_numbers(num_numbers):
    return [random.randint(0, 100000) for _ in range(num_numbers)]

def generate_and_store_subset(instance_id, num_numbers):
    # Generate a subset of random numbers
    random_numbers = generate_random_numbers(num_numbers)
   
    # Store each number in Google Cloud Storage
    bucket = storage_client.get_bucket(bucket_name)
    for number in random_numbers:
        blob = bucket.blob(f"{instance_id}_{number}")
        blob.upload_from_string(str(number))


