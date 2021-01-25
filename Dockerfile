# thanks to https://blog.bitsacm.in/django-on-docker/
FROM python:slim as fundamental

# entrypoint.sh is using netcat to wait for db to start up
RUN apt-get update && apt-get install -y netcat

# create an app user in the app group
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash django

# project's src home directory
ENV PROJECT_HOME=/home/django/project

# create required directories
RUN mkdir -p $PROJECT_HOME/static

# cd to working dir
WORKDIR $PROJECT_HOME

# get the pip requirements file
COPY requirements.txt .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# start the entrypoint script
ENTRYPOINT ["./django-entrypoint.sh"]

#
# development build target
#
FROM fundamental as development

# setup python for development
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# setup django for development
ENV DJANGO_DEBUG True

#
# production build target
#
FROM fundamental as production

# setup python for production
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# setup django for development
ENV DJANGO_DEBUG False

# copy src into container
COPY app app
COPY project project
COPY manage.py .
COPY django-entrypoint.sh .
RUN chmod a+x django-entrypoint.sh

# adjust ownership
RUN chown -R django:django .

# drop privs
USER django:django
