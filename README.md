# aiobanking
Architecture PoC showing event sourcing for banking use cases




# Run this PoC

```
# load root user
docker-compose run sor python manage.py loaddata fixtures/users.json

# load test data
docker-compose run sor python manage.py loaddata current/fixtures/current.json

# Start
docker-compose up -d

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
docker exec -i -t -u root $(docker ps | grep soi_kafka | cut -d' ' -f1) /bin/bash

# list topics
$KAFKA_HOME/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list
```