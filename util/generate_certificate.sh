#!/usr/bin/env bash

# Generate a root certificate
# Each other certificate is signed using this root certificate

NUMBER_OF_DAYS=100
ROOT_CERTIFICATE_KEY="cert/rootCA.key"
ROOT_CERTIFICATE_NAME="cert/rootCA.pem"
LENGTH_OF_CERTIFICATE=4096
CERTIFICATE_TYPE=x509
HASH_ALGORITHM=sha512

generate_root_ca() {
  openssl genrsa \
    -des3 \
    -out $ROOT_CERTIFICATE_KEY $LENGTH_OF_CERTIFICATE

  openssl req -$CERTIFICATE_TYPE \
    -new \
    -nodes -key $ROOT_CERTIFICATE_KEY \
    -$HASH_ALGORITHM \
    -days $NUMBER_OF_DAYS \
    -out $ROOT_CERTIFICATE_NAME \
    -config server.csr.cnf
}

create_server_certificate() {
  openssl req \
    -new -$HASH_ALGORITHM \
    -nodes \
    -out server.csr \
    -newkey rsa:$LENGTH_OF_CERTIFICATE \
    -keyout cert/server.key \
    -config cert/server.csr.cnf

  openssl x509 \
    -req -in cert/server.csr \
    -CA $ROOT_CERTIFICATE_NAME \
    -CAkey $ROOT_CERTIFICATE_KEY \
    -CAcreateserial -out cert/server.crt \
    -days $NUMBER_OF_DAYS \
    -$HASH_ALGORITHM \
    -extfile v3.ext
}

main() {
  generate_root_ca
  create_server_certificate
}

main
