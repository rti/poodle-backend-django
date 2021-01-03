#!/bin/sh
# thanks to https://blog.bitsacm.in/django-on-docker/

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations app --noinput
python manage.py migrate --noinput

exec "$@"

