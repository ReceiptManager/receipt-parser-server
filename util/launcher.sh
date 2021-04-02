#!/usr/bin/env bash

IP=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')

echo "Current IP is: $IP"
docker run --rm -t -i -p $IP:8721:8721 -v "$(pwd)/data:/app/data" -v "$(pwd):/config" -e RECEIPT_PARSER_CONFIG_DIR="/config" monolidth/receipt-parser
