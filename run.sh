#!/bin/sh
rm -rf .env
touch .env
echo "username=$1" >> .env
echo "password=$2" >> .env
echo "port=$3" >> .env
python3 main.py