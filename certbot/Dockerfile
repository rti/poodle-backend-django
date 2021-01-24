# FROM certbot/certbot:latest
FROM debian:buster-slim

RUN apt-get update
RUN apt-get install -y openssl certbot netcat inetutils-ping
# TODO cleanup

COPY entrypoint.sh /
RUN chmod a+x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]

