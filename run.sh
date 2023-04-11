#!/bin/sh
apk --update-cache add python3 py3-pip
pip3 install -r requirements.txt
rm -rf .env
touch .env
echo "username=$1" >> .env
echo "password=$2" >> .env
python3 app.py