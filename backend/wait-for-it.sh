#!/bin/sh

set -e

host="$1"
shift

until nc -z "$host" 5432; do
  echo  "Waiting for postgres..."
  sleep 1
done

echo "Postgres is up!"

exec "$@"
