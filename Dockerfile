# thanks to https://blog.bitsacm.in/django-on-docker/
FROM python:slim

# these two environment variables prevent __pycache__/ files
#ENV PYTHONUNBUFFERED 1
#ENV PYTHONDONTWRITEBYTECODE 1

# these two environment variables allow __pycache__/ files
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# entrypoint.sh is using netcat to wait for db to start up
RUN apt-get update && apt-get install -y netcat

# create an app user in the app group
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash django

# project's src home directory
ENV PROJECT_HOME=/home/django/project

# create the staticfiles directory # TODO do we need static files?
RUN mkdir -p $PROJECT_HOME/static

# cd to working dir
WORKDIR $PROJECT_HOME

# get the pip requirements file
COPY requirements.txt .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy src into container # TODO: disable for development
COPY . $PROJECT_HOME

# adjust ownership
RUN chown -R django:django $PROJECT_HOME

# drop privs
USER django:django

# start the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
