
#!/bin/sh

DOMAIN="api.poodle.rtti.de"

CERT_VALID_TIME_MIN=$((60 * 60 * 24 * 30 * 2))
CERT_CHECK_INTERVAL=$((60 * 60 * 24))

LETSENCRYPT_DIR="/etc/letsencrypt"
CURRENT_CERTS_DIR="$LETSENCRYPT_DIR/live"
CURRENT_CERT="$CURRENT_CERTS_DIR/$DOMAIN/fullchain.pem"


current_date_time() {
  date +%s
}

current_cert_valid_until() {
  date -d "`openssl x509 -enddate -noout -in $CURRENT_CERT | sed 's/notAfter=//'`" +%s
}

current_cert_time_remaining() {
  echo $((`current_cert_valid_until` - `current_date_time`))
}

current_cert_check_and_renew() {
  echo "Certificate valid for $(( `current_cert_time_remaining` / 60 / 60 / 24 )) days."
  echo "Renew threshold is $(( $CERT_VALID_TIME_MIN / 60 / 60 / 24 )) days."

  if [ `current_cert_time_remaining` -lt $CERT_VALID_TIME_MIN ]; then
    echo "Requesting new certificate."
    certbot renew
  else
    echo "Certificate ok."
  fi
}

main() {
  while true; do 
    echo "Checking current certificate."
    current_cert_check_and_renew
    sleep $CERT_CHECK_INTERVAL
  done
}

main

