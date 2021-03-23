#!/usr/bin/env bash

API_PATH="${PWD}/.api_token"

# generate api token if non exists
if [ ! -f "$API_PATH" ];then
  echo $(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '') > $API_PATH
else
  if [ "$(cat $API_PATH | tr -d " ")" = "" ];then
    rm -f $API_PATH
    echo $(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '') > $API_PATH
  fi
fi