FROM python:slim as core
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir -p /srv/project
WORKDIR /srv/project
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat
ENTRYPOINT ["/srv/project/entrypoint.sh"]
