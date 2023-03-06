# Mqtt-PostgreSQL-Docker
___
## Description: 
Design, write in Python 3 and run a prototype application that processes measurement data
from the MQTT message broker. Aggregate data at intervals of T seconds and save the following result in
PostgreSQL after obtaining N measurements for the aggregation period.

___
## Project architecture:

#### Publish_data:
* Publish data(JSON format) to public MQTT broker hosted by "https://console.hivemq.cloud/" 

#### Process_data:
* Subscribe to MQTT broker, retrieving data, Later according to time interval "T" and number measurement "N" aggregates the data and store it to local PostgreSQL database.

#### Store_data:
* Connection to local postgresql database, queries to create and insert aggregated data.

___
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development. 

### Requirements
- Python 3 installed
- Working MQTT broker, to which you can connect
- PostgreSQL, pgAdmin4 installed
- Docker installed 
___
## Installation

### Local Machine

- To publish data
```commandline
Python publish_data.py
```
- Change host connection to PostgreSQL database: from "host.docker.internal" to "localhost"
- To process and store data:
```commandline
Python process_data.py <time interval> <number of measurements>
```

### Docker
#### Docker-compose

- See docker-compose.yml file in repo. To build:

```commandline
docker-compose build 
```

Will build two images. 
#### To run images:
- List of images:
```commandline
docker image ls
```
- Docker image to publish the data:
```commandline
docker run homework_publish
```
- Docker image to process and store data:
```commandline
docker run homework_process <time interval> <number of measurements>
```
