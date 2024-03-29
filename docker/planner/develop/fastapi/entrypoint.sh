#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z database 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Waiting for mongo..."
while ! nc -z document_db 27017; do
  sleep 0.1
done
echo "MongoDB started"

exec "$@"
