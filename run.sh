#!/bin/sh
pip3 install -r requirements.txt
rm -rf .env
touch .env
echo "username=$1" >> .env
echo "password=$2" >> .env
python3 app.py