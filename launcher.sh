#!/usr/bin/env bash

IP=$(echo -n $(hostname --ip-address | tr " " "\n" | grep -v 172.17.0.1))
echo "Current IP is: $IP"
docker run -t -i -p $IP:8721:8721 -v `pwd`/data/img:/app/data/img monolidth/receipt-parser-server
