#!/usr/bin/env bash

API_PATH="${PWD}/data/.api_token"

print_fail() {
    echo -e "\t\033[31m API token is not valid or present\033[0m"
    echo -e "\t\033[31m Generation is required \033[0m"
}

# generate api token if non exists
if [ ! -f "$API_PATH" ];then
  echo "$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '')" > "$API_PATH"
  print_fail
else
  if [ "$(cat "$API_PATH" | tr -d " ")" = "" ];then
    print_fail
    rm -f "$API_PATH"
    echo "$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '')" > "$API_PATH"
  else
    echo -e "\t\033[32m API token is valid \033[0m"
    echo -e "\t\033[32m Generation is not required \033[0m"
  fi
fi
