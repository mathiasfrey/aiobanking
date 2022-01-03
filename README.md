# aiobanking
Architecture PoC showing event sourcing for banking use cases.




# Run this PoC
```
# Start
./docker-compose-up -d

# Populate the database
./populate-db.sh

# Deploy the MySQL connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @sor/cdc-mysql.json

```
## System of Record (SoR)

Visit 127.0.0.1:8000/admin on your machine; log in with user `root` and password `root`.


# Inspect
```
# Log in into the database
docker run -it --rm --network aiobanking_default --name mysqlterm --link aiobanking_mysql_1 --rm mysql:8.0 sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" --host=mysql' 

# log in to Kafka
docker exec -i -t -u root $(docker ps | grep kafka | cut -d' ' -f1) /bin/bash

# list topics
./bin/kafka-topics.sh --list --bootstrap-server kafka:9092

# observe changes
$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic current_currentaccount --from-beginning
```


# Initial setup / Dev hints

```
# create django layout
docker-compose run django django-admin startproject systemofrecord
sudo chown -R $USER sor

# Data & migrations:
docker-compose run sor python manage.py createsuperuser
docker-compose run sor python manage.py migrate
docker-compose run sor python manage.py makemigrations

# Rebuild Image:
docker-compose build django
```




# Acknowledgment
The setup of mysql, kafka and debezium was taken from the [debezium tutorial](https://debezium.io/documentation/reference/1.8/tutorial.html). This was then connected to faust as explained by [David Farrugia](https://towardsdatascience.com/introduction-to-kafka-stream-processing-in-python-e30d34bf3a12). The blog post by
[Benjamin Ramser](https://iwpnd.pw/articles/2020-03/apache-kafka-fastapi-geostream) helped me to set up a frontend listening to websockets fed by a stream.