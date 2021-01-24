#/bin/bash

nginx -g "daemon off;" &

while true; do 
  inotifywait -e create /etc/letsencrypt/live/poodle.rtti.de/; 
  echo "reloading nginx"; 
  nginx -s reload; 
  sleep 1
done
