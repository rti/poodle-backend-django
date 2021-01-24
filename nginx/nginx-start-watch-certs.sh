#/bin/sh

set -e
# set -x

SLEEP_BEFORE_RELOAD=10

watch_certs_and_reload() {
  while true; do
    inotifywait -e create /etc/letsencrypt/live/poodle.rtti.de/;
    echo "cert change detected, waiting $SLEEP_BEFORE_RELOAD seconds before reload";
    sleep $SLEEP_BEFORE_RELOAD
    echo "reloading nginx";
    nginx -s reload;
    echo "done";
  done
}

watch_certs_and_reload &

nginx -g "daemon off;"

