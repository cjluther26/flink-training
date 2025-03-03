# Homework

For this homework we will be using the Taxi data:
- Green 2019-10 data from [here](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz)


## Start Red Panda, Flink Job Manager, Flink Task Manager, and Postgres 

There's a `docker-compose.yml` file in the homework folder (taken from [here](https://github.com/redpanda-data-blog/2023-python-gsg/blob/main/docker-compose.yml))

Copy this file to your homework directory and run

```bash
docker-compose up
```

(Add `-d` if you want to run in detached mode)

Visit `localhost:8081` to see the Flink Job Manager

Connect to Postgres with [DBeaver](https://dbeaver.io/).

The connection credentials are:
- Username `postgres`
- Password `postgres`
- Database `postgres`
- Host `localhost`
- Port `5432`


In DBeaver, run this query to create the Postgres landing zone for the first events:
```sql 
CREATE TABLE processed_events (
    test_data INTEGER,
    event_timestamp TIMESTAMP
)
```


## Sending the taxi data

Now let's send our actual data:

* Read the green csv.gz file
* We will only need these columns:
  * `'lpep_pickup_datetime',`
  * `'lpep_dropoff_datetime',`
  * `'PULocationID',`
  * `'DOLocationID',`
  * `'passenger_count',`
  * `'trip_distance',`
  * `'tip_amount'`

Iterate over the records in the dataframe

```python
for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    print(row_dict)
    break

    # TODO implement sending the data here
```

Note: this way of iterating over the records is more efficient compared
to `iterrows`


## Question 1. Connecting to the Kafka server

We need to make sure we can connect to the server, so
later we can send some data to its topics

First, let's install the kafka connector (up to you if you
want to have a separate virtual environment for that)

```bash
pip install kafka-python
```

You can start a jupyter notebook in your solution folder or
create a script

Let's try to connect to our server:

```python
import json
import time 

from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()
```


## Question 3: Sending the Trip Data

* Create a topic `green-trips` and send the data there
* How much time in seconds did it take? (You can round it to a whole number)
* Make sure you don't include sleeps in your code



