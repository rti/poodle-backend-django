#!/bin/sh
# thanks to https://blog.bitsacm.in/django-on-docker/

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.5
    done

    echo "PostgreSQL started"
fi

echo "Making migrations and migrating the database."
python manage.py makemigrations app --noinput
python manage.py migrate --noinput

echo "Collecting static files."
python manage.py collectstatic --noinput

echo "Done."
echo "Passing on to $@"
exec "$@"

