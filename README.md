# poodle-backend-django

Poodle is a scheduling tool. 

This repository contains the REST API backend implemented in django.

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
