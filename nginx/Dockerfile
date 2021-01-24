FROM nginx:stable

RUN apt-get update && apt-get install -y inotify-tools \
      && apt-get remove --purge --auto-remove -y \
      && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/nginx.list

COPY ssl.conf /etc/nginx/conf.d/
COPY default.conf /etc/nginx/conf.d/

COPY setup-certs.sh /
RUN chmod a+x /setup-certs.sh

COPY nginx-start-watch-certs.sh /
RUN chmod a+x /nginx-start-watch-certs.sh

ENTRYPOINT ["/setup-certs.sh"]
CMD ["/nginx-start-watch-certs.sh"]

