#!/bin/sh
apk --update-cache add python3 py3-pip
pip3 install --break-system-packages -r requirements.txt
rm -rf .env
touch .env
echo "username=$1" >> .env
echo "password=$2" >> .env
echo "port=$3" >> .env
python3 main.py