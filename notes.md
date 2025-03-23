# Flink Training

## Setup
- In home directory of repo, run `docker compose up` to spin up all the entities we need for the lab.
- If needed, make sure that your database tool of choice (DBeaver, DataGrip, PGAdmin) is set up s.t. the data we're working with here in this lab can be browsed & queried. 
    - I'll be using PGAdmin, which I've configured by adding configurations for it to the `docker-compose.yml` file obtained from the source repo. 
    - If you ran `docker compose up` prior to having this code in the `docker-compose.yml`, you'll have to make sure you spin that up, as well. VSCode has a nice little popup that allows you to click and start a single service, which is what I did (it ran `docker compose -f 'docker-compose.yml' up -d --build 'pgadmin'`).
- I had to create a virutal enviroment (using Python 3.10, specifically) in order to set up `apache-flink`. Using my default version of Python, it didn't a version of `numpy` that `apache-flink` was requiring.

## Additional Notes
`producers.py`
- Zach notes that when events are being sent to Kafka, they must be serialized into a format that can be written to disk. In this case, we're just using a basic `json_serializer`. This is the most common option to do this (`Thrift` and `Protobuf` are others, as well) and allows for events to be read via many different languages.

`Flink`
- **source**: entity you're *reading* from!
- **sink**: entity you're *dumping* into!
- When Flink starts, it sets up a **`StreamExecutionEnvironment`**. 
- You can configure this environment. One key way is that it can be set to either `in_streaming_mode()` or `in_batch_mode()` -- the first keeps the job running, listening for events, while the other is executed in batches (like a cron job in Airflow). 
- Flink also has a **`StreamTableEnvironment`**. This is where the understanding of sources and sinks is done.
- **Watermarking**: a watermark is a special event injected into a data stream that carries a timestamp, indicating the progress of event time and signaling when earlier events are considered to have arrived.
    - *"Specifies the tolerance for out-of-sync events."*
    - Ex. in an event stream of timestamps, a watermark with timestamp `10:00` indicates that all events with timestamps before or at `10:00` should have already arrived.


`Kafka`
- When reading from Kafka, you have to be cognizant of **offsets**. These keep track of how much data you've already read from the topic. In configuring a source from Kafka, you have **5 options** for `'scan.startup.mode'`, where we will focus on the *first 2*:
    -  `'earliest-offset'`: when starting up Flink, it will read from the *earliest* event it can.
    - `'latest-offset'`: reads data from the latest available offset in each partition. Essentially, it will **only process new data that comes in, AFTER the job starts!*
    - `'timestamp'`: reads data from a specific timestamp (milliseconds since epoch).
    - `'group-offsets'`: reads data from the committed offsets of a specific consumer group.
    - `'specific-offsets'`: reads data from specific offsets provided for each partition.