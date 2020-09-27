#/usr/bin/env bash

KEY="rsa:4096"
CERTIFICATE_OUTPUT="cert.pem"
KEY_OUTPUT="key.pem"
DAYS=365

openssl req -x509 -newkey $KEY -nodes -out $CERTIFICATE_OUTPUT -keyout  $KEY_OUTPUT -days $DAYS
