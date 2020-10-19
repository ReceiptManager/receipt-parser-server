#!/usr/bin/env bash

# ...............................................
NUMBER_OF_DAYS=100
ROOT_CERTIFICATE_KEY="rootCA.key"
ROOT_CERTIFICATE_NAME="rootCA.pem"
# shellcheck disable=SC2034
LENGTH_OF_CERTIFICATE=4096
CERTIFICATE_TYPE=x509
HASH_ALGORITHM=sha512
# ...............................................

generate_root_ca() {
    openssl genrsa -des3 -out $ROOT_CERTIFICATE_KEY 4096
    openssl req -$CERTIFICATE_TYPE -new -nodes -key $ROOT_CERTIFICATE_KEY -$HASH_ALGORITHM -days $NUMBER_OF_DAYS -out $ROOT_CERTIFICATE_NAME -config server.csr.cnf
}

create_server_certificate() {
  openssl req -new -sha512 -nodes -out server.csr -newkey rsa:4096 -keyout server.key -config server.csr.cnf
  openssl x509 -req -in server.csr -CA $ROOT_CERTIFICATE_NAME -CAkey $ROOT_CERTIFICATE_KEY -CAcreateserial -out server.crt -days $NUMBER_OF_DAYS -$HASH_ALGORITHM -extfile v3.ext
}


main() {
generate_root_ca
create_server_certificate
}

main
