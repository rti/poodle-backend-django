FROM nginx:stable

COPY certbot-ssl.conf /etc/nginx/conf.d/
COPY default.conf /etc/nginx/conf.d/

COPY entrypoint.sh /docker-entrypoint.d/99-setup-certs.sh
RUN chmod a+x /docker-entrypoint.d/99-setup-certs.sh

