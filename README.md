# django-rest-api

An opinionated project template for creating REST APIs

## Based on

 - Django https://www.djangoproject.com/
 - Django REST framework https://www.django-rest-framework.org/
 - Django CORS Headers https://pypi.org/project/django-cors-headers/
 - Token Auth https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
 - Postgres https://www.postgresql.org/
 - Docker https://www.docker.com/
 - Docker Compose https://docs.docker.com/compose/
 - Vim Rest Console https://github.com/diepm/vim-rest-console

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
## TODO

 - Production setup
   - Docker: include source in container, remove volume
   - Docker: postgres auth
   - Docker: nginx proxy, SSL
   - Django: disable debug mode
   - Django: set SECRET_KEY
   - Django: configure CORS_ALLOWED_ORIGINS

  
