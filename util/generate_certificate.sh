#!/usr/bin/env bash

NUMBER_OF_DAYS=100
ROOT_CERTIFICATE_KEY="cert/rootCA.key"
ROOT_CERTIFICATE_NAME="cert/rootCA.pem"
PRIVATE_KEY_FILE=".private_key"
LENGTH_OF_CERTIFICATE=4096
CERTIFICATE_TYPE=x509
HASH_ALGORITHM=sha512

generate_root_ca() {
  openssl genrsa \
    -des3 \
    -passout file:$PRIVATE_KEY_FILE\
    -out $ROOT_CERTIFICATE_KEY $LENGTH_OF_CERTIFICATE 

  openssl req -$CERTIFICATE_TYPE \
    -new \
    -nodes -key $ROOT_CERTIFICATE_KEY \
    -$HASH_ALGORITHM \
    -days $NUMBER_OF_DAYS \
    -out $ROOT_CERTIFICATE_NAME \
    -passin file:$PRIVATE_KEY_FILE\
    -config cert/server.csr.cnf
}

create_server_certificate() {
  openssl req \
    -new -$HASH_ALGORITHM \
    -nodes \
    -out cert/server.csr \
    -passin file:$PRIVATE_KEY_FILE \
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
    -passin file:$PRIVATE_KEY_FILE\
    -extfile cert/v3.ext
}

submit_password() {
    if [ ! -f ".private_key" ];then
        echo "Submit default password"
        echo "change_me"  > $PRIVATE_KEY_FILE
    fi
}

main() {
  if [ ! -f ".private_key" ];then
    submit_password
    generate_root_ca
    create_server_certificate
  else
    echo -e "\t \033[32m Certificate is already present. \033[0m"
    echo -e "\t \033[32m Generation is not required \033[0m"
  fi
}

main
