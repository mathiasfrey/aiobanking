#!/bin/sh

echo ">>> create db"
docker-compose run sor python manage.py migrate

echo ">>> load root user"
docker-compose run sor python manage.py loaddata fixtures/users.json

echo ">>> load test data"
docker-compose run sor python manage.py loaddata current/fixtures/current.json

echo ">>> starting docker"
docker-compose up -d

echo ">>> creating a CDC connector"
# first, create a db user
docker exec -i -t postgres /bin/bash
psql --user postgres
CREATE USER debezium WITH password 'dbz';
#ALTER ROLE "debezium" WITH LOGIN;
#ALTER ROLE "debezium" WITH REPLICATION;
#GRANT ALL PRIVILEGES ON DATABASE db TO debezium;
ALTER USER debezium WITH SUPERUSER;

# create connector
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "currentaccounts-connector99", "config": { "connector.class": "io.debezium.connector.postgresql.PostgresConnector", "database.hostname": "db", "database.port": "5432", "database.user": "debezium", "database.password": "dbz", "database.dbname": "db", "database.server.name": "db", "table.include.list": "current_currentaccount", "database.history.kafka.bootstrap.servers": "kafka:9092", "database.history.kafka.topic": "schema-changes.currentaccount", "plugin.name": "pgoutput"} }'