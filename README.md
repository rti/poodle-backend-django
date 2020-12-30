# poodle-backend-django

An opinionated project template for creating REST APIs

## Based on

 - https://github.com/rti/django-rest-api

## How to use

Install docker-compose

### Start the API

```shell
docker-compose up
```

Direct your browser to http://127.0.0.1:8000/app/

### Access the django admin interface

```shell
docker-compose run --rm django python manage.py createsuperuser
docker-compose up
```

Direct your browser to http://127.0.0.1:8000/admin/

### Run tests

```shell
docker-compose run --rm django python manage.py test --noinput --failfast
```
