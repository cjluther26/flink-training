import json
from time import time

import gzip 
import csv 
import urllib.request

from kafka import KafkaProducer

file_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz'
local_file = 'green_tripdata_2019-10.csv.gz'

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()

t0 = time()

topic_name = 'green-trips'

selected_columns = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount'
]

with urllib.request.urlopen(file_url) as response:
    with gzip.GzipFile(fileobj=response) as f:
        reader = csv.DictReader(f.read().decode('utf-8').splitlines())

        # Produce each row to the Kafka topic
        for row in reader:
            # Filter for only the columns we want
            filtered_row = {key: row[key] for key in selected_columns if key in row}
            producer.send(topic_name, filtered_row)
            print(f"Sent: {filtered_row}")

producer.flush()

t1 = time()
print(f'took {(t1 - t0):.2f} seconds')

# producer.bootstrap_connected()