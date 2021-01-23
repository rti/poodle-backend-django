FROM nginx:stable

COPY certbot-ssl.conf /etc/nginx/conf.d/
COPY default.conf /etc/nginx/conf.d/

COPY 50-setup-certs.sh /docker-entrypoint.d
RUN chmod a+x /docker-entrypoint.d/50-setup-certs.sh

