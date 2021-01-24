#!/bin/sh

set -e
# set -x

DOMAIN_NAME=poodle.rtti.de

PATH_LETSENCRYPT=/etc/letsencrypt

FILE_DHPARAMS=$PATH_LETSENCRYPT/dhparams.pem
FILE_CHAIN=$PATH_LETSENCRYPT/live/$DOMAIN_NAME/fullchain.pem
FILE_KEY=$PATH_LETSENCRYPT/live/$DOMAIN_NAME/privkey.pem

SIZE_DHPARAMS=1024
SIZE_KEY=4096

mkdir -p $PATH_LETSENCRYPT/live/$DOMAIN_NAME/

if [ ! -e $FILE_DHPARAMS ]; then
  echo "### generating $FILE_DHPARAMS..."
  openssl dhparam -out $FILE_DHPARAMS $SIZE_DHPARAMS
  echo "### done"
else
  echo "### using existing $FILE_DHPARAMS."
fi

if [ ! -e $FILE_KEY ] || [ ! -e $FILE_CHAIN ]; then
  echo "### generating $FILE_CHAIN and $FILE_KEY..."
  openssl req -x509 -nodes -newkey rsa:$SIZE_KEY -days 1 \
    -keyout $FILE_KEY -out $FILE_CHAIN -subj "/CN=$DOMAIN_NAME"
  echo "### done"
else
  echo "### using existing $FILE_CHAIN and $FILE_KEY."
fi

echo "### starting $@"
exec $@
