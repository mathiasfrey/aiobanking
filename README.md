# aiobanking
Architecture PoC showing event sourcing for banking use cases




# Run this PoC

```
# Start
./start.sh
```
Visit 127.0.0.1:8000 on your machine.


# Initial setup / Dev hints

```
docker-compose run sor django-admin startproject systemofrecord
sudo chown -R $USER sor
```

## Data & migrations:

```
docker-compose run sor python manage.py createsuperuser
docker-compose run sor python manage.py migrate
docker-compose run sor python manage.py makemigrations
```

## Rebuild Image:
```
docker-compose build sor
```

## Kafka tools
```
# Enter Kafka
docker exec -i -t -u root $(docker ps | grep kafka | cut -d' ' -f1) /bin/bash

# list topics
$KAFKA_HOME/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list
```

## db & CDC
```
docker-compose up -d

# Deploy the MySQL connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @sor/cdc-mysql.json

# Log in into the database
docker run -it --rm --network aiobanking_default --name mysqlterm --link aiobanking_mysql_1 --rm mysql:8.0 sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" --host=mysql' 

# log in to the connector
docker exec -i -t aiobanking_kafka_1
# list topics
./bin/kafka-topics.sh --list --bootstrap-server kafka:9092

# observe changes
./bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic products --from-beginning

```

# Acknowledgment

The Kafka setup including source code was taken from [David Farrugia](https://towardsdatascience.com/introduction-to-kafka-stream-processing-in-python-e30d34bf3a12)

