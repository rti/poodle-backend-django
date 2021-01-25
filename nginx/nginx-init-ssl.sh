#!/bin/sh

set -e
# set -x

DOMAIN_NAME=api.poodle.rtti.de

PATH_LETSENCRYPT=/etc/letsencrypt

FILE_DHPARAMS=$PATH_LETSENCRYPT/dhparams.pem
FILE_CHAIN=$PATH_LETSENCRYPT/live/$DOMAIN_NAME/fullchain.pem
FILE_KEY=$PATH_LETSENCRYPT/live/$DOMAIN_NAME/privkey.pem

SIZE_DHPARAMS=4096
SIZE_KEY=4096

mkdir -p $PATH_LETSENCRYPT/live/$DOMAIN_NAME/

if [ ! -e $FILE_DHPARAMS ]; then
  echo "Generating $FILE_DHPARAMS..."
  openssl dhparam -out $FILE_DHPARAMS $SIZE_DHPARAMS
  echo "Done."
else
  echo "Using existing $FILE_DHPARAMS."
fi

if [ ! -e $FILE_KEY ] || [ ! -e $FILE_CHAIN ]; then
  echo "Generating $FILE_CHAIN and $FILE_KEY..."
  openssl req -x509 -nodes -newkey rsa:$SIZE_KEY -days 1 \
    -keyout $FILE_KEY -out $FILE_CHAIN -subj "/CN=$DOMAIN_NAME"
  echo "Done."
else
  echo "Using existing $FILE_CHAIN and $FILE_KEY."
fi

echo "Done."
echo "Passing on to $@"
exec "$@"
