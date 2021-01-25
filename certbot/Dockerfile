FROM debian:buster-slim

RUN apt-get update
RUN apt-get install -y openssl certbot netcat\
      && apt-get remove --purge --auto-remove -y \
      && rm -rf /var/lib/apt/lists/*

COPY certbot-init.sh /
RUN chmod a+x /certbot-init.sh

COPY certbot-auto-renew.sh /
RUN chmod a+x /certbot-auto-renew.sh

ENTRYPOINT ["/certbot-init.sh"]
CMD ["/certbot-auto-renew.sh"]
