#!/bin/sh

# set -x
set -e

DOMAIN="api.poodle.rtti.de"
EMAIL="mail@rtti.de"
# enable for testing
# STAGING="--staging"

RSA_KEY_SIZE=4096
# testing only
# RSA_KEY_SIZE=1024

LETSENCRYPT_DIR="/etc/letsencrypt"
CURRENT_CERTS_DIR="$LETSENCRYPT_DIR/live/$DOMAIN"
CURRENT_CERT="$CURRENT_CERTS_DIR/fullchain.pem"

wait_for_nginx() {
  echo "Waiting for nginx..."
  while ! nc -z nginx 80; do
    sleep 0.5
  done

  echo "Nginx started"
}

main() {
  wait_for_nginx

  cert_issuer=`openssl x509 -issuer -noout -in $CURRENT_CERT`

  if [ "$cert_issuer" = "issuer=CN = $DOMAIN" ]; then
    echo "Found self signed certificate."

    echo "Moving to $LETSENCRYPT_DIR/selfsigned-bootstrap-cert."
    mv $CURRENT_CERTS_DIR $LETSENCRYPT_DIR/selfsigned-bootstrap-cert

    certbot certonly --webroot -w /var/www/certbot \
      $STAGING \
      --email $EMAIL \
      -d $DOMAIN \
      --rsa-key-size $RSA_KEY_SIZE \
      --agree-tos \
      --no-eff-email
  else
    echo "Ok, certificate is not self signed."
  fi

  echo "Done."
}

main

echo "Passing on to $@"
exec "$@"
