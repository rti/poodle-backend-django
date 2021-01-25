#!/bin/sh

# set -x
set -e

DOMAIN="api.poodle.rtti.de"
EMAIL="mail@rtti.de"

RSA_KEY_SIZE=4096

LETSENCRYPT_DIR="/etc/letsencrypt"
CURRENT_CERTS_DIR="$LETSENCRYPT_DIR/live/$DOMAIN"
CURRENT_CERT="$CURRENT_CERTS_DIR/fullchain.pem"

wait_for_nginx() {
  while ! nc -z nginx 80; do
    echo "Waiting for nginx..."
    sleep 1
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

    staging_arg="--staging"

    certbot certonly --webroot -w /var/www/certbot \
      $staging_arg \
      --email $EMAIL \
      -d $DOMAIN \
      --rsa-key-size $RSA_KEY_SIZE \
      --agree-tos \
      --no-eff-email

  else
    echo "Ok, certificate is not self signed."
  fi

  echo "Done."
  echo "Passing on to $@"
  exec "$@"
}

main


